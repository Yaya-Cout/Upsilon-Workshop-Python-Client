"""Client for the Upsilon Workshop - Calculator backup handler."""
import logging
import os

import upsilon_py

logger = logging.getLogger(__name__)


async def upload(path: str) -> None:
    """Backup the calculator."""
    logger.info("Uploading %s to the calculator...", path)

    # Get the calculator
    calculator = upsilon_py.NumWorks()
    await calculator.start()

    print("Please plug your calculator to your computer.")
    await calculator.connect()

    # Backup the calculator
    storage = await calculator.backup_storage()

    # If the path is a directory, upload all the files in the directory
    if os.path.isdir(path):
        for file in os.listdir(path):
            add_file(os.path.join(path, file), storage)
    else:
        # Add the file to the storage
        add_file(path, storage)

    # Upload the storage
    await calculator.install_storage(storage)

    logger.info("File %s uploaded to the calculator.", path)


def add_file(path, storage) -> None:
    """Add the file to the storage."""
    # Get the records
    records = storage["records"]

    # Create the file
    record = {
        "name": os.path.basename(path).split(".")[0],
        "type": "py",
        "code": "",
        "autoImport": True,
    }
    # Ensure that the file is not already in the storage
    file_in_storage = False
    for file in records:
        if file["name"] == os.path.basename(path).split(".")[0]:
            file_in_storage = True
            break

    if file_in_storage:
        overwrite = input(f"File {os.path.basename(path)} already exists in "
                          "the storage. Overwrite? [y/N] ")
        if overwrite.lower() != "y":
            return

        # Save the file metadata
        if "autoImport" in file:
            file["autoImport"] = file["autoImport"]

        # Delete the file from the storage
        del records[records.index(file)]

        logger.info("File %s deleted from the storage.",
                    os.path.basename(path))

    # Get the file name
    file_name = os.path.basename(path)

    # Get the file content
    with open(path, "rb") as file:
        file_content = str(file.read()).replace("b'", "").replace("'", "")\
            .replace("\\n", "\n")

    record["code"] = file_content

    # Add the file to the storage
    records.append(record)
