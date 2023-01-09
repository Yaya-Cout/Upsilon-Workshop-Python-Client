"""Client for the Upsilon Workshop - Project pulling handler."""
# Standard Library
import logging
import os
import sys
import datetime
import json
import hashlib

# Internal
import upsilon_workshop_client.api.project
import upsilon_workshop_client.utils.clone

logger = logging.getLogger(__name__)


def pull(path: str) -> None:
    """Push a project."""
    logger.debug("Pulling project %s.", path)

    # Read the project info
    project_info = read_project_info(path)

    # Get the project from the server
    server_project = upsilon_workshop_client.api.project.get_project(
        project_info["url"])

    # Compare the modification times
    if server_project.modified > project_info["modified"]:
        logger.debug("Server project is newer than local project.")
        logger.debug("Server project: %s", server_project.modified)
        logger.debug("Local project: %s", project_info["modified"])
        logger.info("Pulling project from server.")

        # Pull the project from the server
        pull_project_from_server(server_project, project_info, path)
    elif server_project.modified < project_info["modified"]:
        logger.error("Local project is newer than server project.")
        logger.debug("Server project: %s", server_project.modified)
        logger.debug("Local project: %s", project_info["modified"])
        sys.exit(1)
    else:
        logger.debug("Server project is the same as local project.")
        logger.debug("Server project: %s", server_project.modified)
        logger.debug("Local project: %s", project_info["modified"])
        logger.info("Project is up to date.")


def read_project_info(path: str) -> dict[str, str | datetime.datetime | int]:
    """Read the project info from the project."""
    # Get the real path
    realpath = os.path.realpath(path)

    # Get the project info
    project_info_path = f"{realpath}/.project_info.json"
    try:
        with open(project_info_path, "r", encoding="utf-8")\
                as project_info_file:
            project_info = json.load(project_info_file)
    except FileNotFoundError:
        logger.error("Project info file not found.")
        sys.exit(1)

    # Parse the modified time
    project_info["modified"] = datetime.datetime.fromisoformat(
        project_info["modified"])

    return project_info


def pull_project_from_server(project:
                             upsilon_workshop_client.api.project.Project,
                             project_info: dict[str, str | datetime.datetime |
                                                int],
                             path: str) -> None:
    """Pull a project from the server."""
    # Get the real path
    realpath = os.path.realpath(path)

    # Get the changed files
    locally_changed_files, distantly_changed_files = get_changed_files(
        project, project_info, realpath)

    if changed_files := [
        file
        for file in locally_changed_files
        if file in distantly_changed_files
    ]:
        logger.warning("Local files have changed.")
        logger.warning("Files: %s", changed_files)
        logger.warning("Pulling anyway will overwrite these files.")
        logger.warning("Do you want to continue? [y/N]")
        answer = input()
        if answer.lower() != "y":
            logger.info("Pull aborted.")
            print("Pull aborted.")
            sys.exit(1)
    elif not locally_changed_files and not distantly_changed_files:
        logger.info("Project is up to date.")
        print("Project is up to date.")

    # Save the server files to the directory
    for server_file in project.files:
        with open(f"{realpath}/{server_file['name']}", "w", encoding="utf-8")\
                as file_object:
            file_object.write(server_file["content"])

    # Remove the local files that have been deleted on the server
    for file in locally_changed_files:
        if file not in project.files:
            os.remove(f"{realpath}/{file}")

    # Update the project info
    upsilon_workshop_client.utils.clone.save_project_info(
        project, realpath)


def get_changed_files(project:
                      upsilon_workshop_client.api.project.Project,
                      project_info: dict[str, str | datetime.datetime | int],
                      path: str) -> tuple[list[str], list[str]]:
    """Get the changed files."""
    # Get the checksums of the local files
    local_checksums = upsilon_workshop_client.utils.clone.\
        generate_checksums(path)

    # Get the checksums of the server files
    server_checksums = {
        file["name"]: upsilon_workshop_client.utils.clone.hashlib.sha256(
            file["content"].encode("utf-8")
        ).hexdigest()
        for file in project.files
    }

    # Get the local checksums from the project info
    project_info_checksums: dict[str, str] = project_info["checksums"]

    locally_changed_files = [
        file
        for file in local_checksums
        if file not in project_info_checksums
        or local_checksums[file] != project_info_checksums[file]
    ]

    server_changed_files: list[str] = [
        file
        for file, value in server_checksums.items()
        if file not in project_info_checksums
        or value != project_info_checksums[file]
    ]

    # Handle the case where a file has been deleted
    for file in project_info_checksums:
        if file not in local_checksums:
            locally_changed_files.append(file)


    return locally_changed_files, server_changed_files
