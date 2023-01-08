"""Client for the Upsilon Workshop - Project initialization handler."""
# Standard Library
import logging
import os
import getpass
import sys
import requests
import json

# Internal
import upsilon_workshop_client.utils.push
import upsilon_workshop_client.utils.clone
import upsilon_workshop_client.api

logger = logging.getLogger(__name__)


def init(path: str, url: str) -> None:
    """Init a project."""
    logger.info("Initializing project %s.", path)

    payload: dict[str, str | list[dict[str, str]]] = {}

    # Create the payload
    add_project_name_and_description(path, payload)
    add_language(path, payload)
    upsilon_workshop_client.utils.push.extract_files(path, payload)

    # Ask for confirmation
    print("The following payload will be sent:")
    print(payload)
    if input("Continue? [y/N] ").lower() != "y":
        logger.debug("Aborting.")
        print("Aborting.")
        return

    # Ask the credentials
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    # Send the request with the credentials
    response = requests.post(
        f"{url}/scripts/",
        json=payload,
        auth=(username, password),
        timeout=10
    )

    # Check the response
    if response.status_code == 201:
        logger.info("Project published successfully. Initializing local "
                    "project...")
        logger.debug("Response: %s", response.text)
    else:
        logger.error("Error while initializing the project: %s", response.text)
        sys.exit(1)

    # Create the metadata files
    project = upsilon_workshop_client.api.project.Project(
        json.loads(response.text)
    )

    # Create the README.md
    upsilon_workshop_client.utils.clone.create_readme(project, path)

    # Create the .project_info.json
    upsilon_workshop_client.utils.clone.save_project_info(project, path)


def add_project_name_and_description(path: str, payload:
                                     dict[
                                         str,
                                         str | list[dict[str, str]]
                                     ]) -> None:
    """Add the project name and description to the payload."""
    # Get the real path
    realpath = os.path.realpath(path)

    # Get the name of the project
    basename = os.path.basename(realpath)

    # Try to get the name from the README.md (first line, without "# ")
    try:
        with open(os.path.join(realpath, "README.md"), "r", encoding="utf-8")\
                as readme:
            name = readme.readline().strip("# ")
            description = readme.read().strip()
    except FileNotFoundError:
        name = basename
        description = ""
        logger.warning("No README.md file found, using the basename as name "
                       "and an empty description.")

    payload["name"] = name
    payload["description"] = description


def add_language(path: str, payload: dict[str, str | list[dict[str, str]]])\
        -> None:
    """Add the language to the payload."""
    # Get the real path
    realpath = os.path.realpath(path)

    # Guess the language based on the files
    files = os.listdir(realpath)

    if [i for i in files if i.endswith(".xw")]:
        payload["language"] = "xcas-python-pow"
    elif [i for i in files if i.endswith(".py")]:
        payload["language"] = "python"
    else:
        logger.warning("No supported language found. Using python.")
        payload["language"] = "python"
    logger.info("Language guessed as %s.", payload["language"])
