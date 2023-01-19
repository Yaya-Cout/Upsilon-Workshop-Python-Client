"""Client for the Upsilon Workshop - Calculator backup handler."""
import logging
import os

import upsilon_py

logger = logging.getLogger(__name__)


async def backup(path):
    """Backup the calculator."""
    logger.info("Backing up calculator to %s...", path)

    # Get the calculator
    calculator = upsilon_py.NumWorks()
    await calculator.start()

    print("Please plug your calculator to your computer.")
    await calculator.connect()

    # Backup the calculator
    storage = await calculator.backup_storage()

    # Save the calculator to the directory
    save_calculator_to_directory(path, storage)

    logger.info("Calculator backed up to %s.", path)


def save_calculator_to_directory(path: str, storage: dict) -> None:
    """Save the calculator to a directory."""
    # Get the real path
    realpath = os.path.realpath(path)

    # Ask the user if they want to overwrite the directory if it already exists
    if os.path.exists(realpath):
        overwrite = input(f"Path '{realpath}' already exists. "
                          "Overwrite? [y/N] ")
        if overwrite.lower() == "y":
            logger.debug("Overwriting path '%s'.", realpath)
        else:
            logger.debug("Aborting.")
            print("Aborting.")
            return

    # Create the directory
    os.makedirs(realpath, exist_ok=True)

    # Create the files
    create_files(realpath, storage)


def create_files(path: str, storage: dict) -> None:
    """Create the files."""
    # Create the files
    for file in storage["records"]:
        if "code" not in file:
            continue
        # Get the file path
        file_path = f"{path}/{file['name'] + '.' + file['type']}"

        # Create the directory
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Create the file
        with open(file_path, "w") as f:
            f.write(file["code"])

        # Print the file path
        print(file_path)
