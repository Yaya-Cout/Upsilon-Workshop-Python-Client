"""Client for the Upsilon Workshop - Project pushing handler."""
# Standard Library
import logging
import os
import sys
import json
import getpass

import requests

import upsilon_workshop_client.api.project
import upsilon_workshop_client.utils.clone

logger = logging.getLogger(__name__)


def push(path: str) -> None:
    """Push a project."""
    logger.debug("Pushing project %s.", path)

    payload: dict[str, str | list[dict[str, str]]] = {}

    # Generate the project
    extract_project_name_and_description(path, payload)
    extract_from_project_info(path, payload)
    extract_files(path, payload)

    # Ask the credentials
    username = input("Username: ")

    # Password is hidden
    password = getpass.getpass("Password: ")

    # Send the request with the credentials
    response = requests.put(
        payload["url"],
        json=payload,
        auth=(username, password),
        timeout=10
    )

    # Check the response
    if response.status_code == 200:
        logger.info("Project pushed successfully.")
    else:
        logger.error("Error while pushing the project: %s", response.text)
        sys.exit(1)

    # Update the project_info.json
    upsilon_workshop_client.utils.clone.save_project_info(
        upsilon_workshop_client.api.project.Project(response.json()),
        path
    )


def extract_project_name_and_description(path: str, payload:
                                         dict[
                                             str,
                                             str | list[dict[str, str]]
                                         ]) -> None:
    """Extract the project name from the path."""
    # Get the real path
    realpath = os.path.realpath(path)

    # Get the name of the project
    basename = os.path.basename(realpath)

    # Try to get the name from the README.md (first line, without "# ")
    try:
        with open(f"{realpath}/README.md", "r", encoding="utf-8") as f:
            name = f.readline().replace("# ", "").strip()

            # Description is the rest of the file (without the first line and
            # the trailing newline)
            payload["description"] = f.read().strip()

        # Check if the name is the same as the basename
        if name != basename:
            logger.warning("Name from README.md (%s) is different from "
                           "basename (%s). Using README.md name instead.",
                           name, basename)
        payload["name"] = name
    except FileNotFoundError:
        logger.debug("README.md not found, using basename. Description will "
                     "be empty.")
        payload["name"] = basename
        payload["description"] = ""


def extract_from_project_info(path: str, payload: dict[str, str | list[
                                                       dict[str, str]]])\
        -> None:
    """Extract the project name from the project info file."""
    # Get the real path
    realpath = os.path.realpath(path)

    # Try to get the info from the project_info.json
    try:
        with open(
            f"{realpath}/.project_info.json",
            "r",
            encoding="utf-8"
        ) as f:
            project_info = json.load(f)
            for i in [
                "url", "language", "version", "licence", "compatibility"
            ]:
                if i in project_info:
                    payload[i] = project_info[i]
                else:
                    # TODO: Try to restore the missing info from the server
                    logger.error("Project info file is missing %s. Exiting.",
                                 i)
                    sys.exit(1)
    except FileNotFoundError:
        logger.error("Project info file not found. Exiting.")
        sys.exit(1)


def extract_files(path: str, payload: dict[str, str | list[dict[str, str]]])\
        -> None:
    """Extract the files from the project."""
    # Get the real path
    realpath = os.path.realpath(path)

    # Create the files list
    payload["files"] = []

    # If the path is a file, add it to the list
    if os.path.isfile(realpath):
        add_file_to_list(os.path.dirname(realpath), os.path.basename(realpath),
                         path, payload)

        # Change the file name
        payload["files"][0]["name"] = os.path.basename(path)
        return

    # Iterate over the files
    for root, _, files in os.walk(realpath):
        for file in files:
            # Ignore the project info file and the README.md
            if file in [".project_info.json", "README.md"]:
                continue

            # Add the file to the list
            add_file_to_list(root, file, path, payload)


def add_file_to_list(root: str, file: str, path: str,
                     payload: dict[str, str | list[dict[str, str]]]) -> None:
    # Get the real path
    realpath = os.path.realpath(f"{root}/{file}")

    # Get the relative path
    relativepath = os.path.relpath(realpath, path)

    # Get the file content
    with open(realpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Add the file to the list
    payload["files"].append({
        "name": relativepath,
        "content": content
    })
