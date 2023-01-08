"""Client for the Upsilon Workshop - Project cloning handler."""
# Standard Library
import logging
import os
import json

# Internal
import upsilon_workshop_client.api.project

logger = logging.getLogger(__name__)


def clone(project_url: str, path: str) -> None:
    """Clone a project."""
    logger.info("Cloning project %s to %s...", project_url, path)

    # Get the project
    project = upsilon_workshop_client.api.project.get_project(project_url)

    project_path = f"{path}/{project.name}"

    # If the path already exists, ask the user if they want to overwrite it
    if os.path.exists(project_path):
        overwrite = input(f"Path '{project_path}' already exists. "
                          "Overwrite? [y/N] ")
        if overwrite.lower() == "y":
            logger.debug("Overwriting path '%s'.", project_path)
        else:
            logger.debug("Aborting.")
            print("Aborting.")
            return

    # Save the project to the directory
    save_project_to_directory(project, project_path)


def save_project_to_directory(project:
                              upsilon_workshop_client.api.project.Project,
                              path: str) -> None:
    """Save a project to a directory to apply the clone."""
    # Get the real path
    realpath = os.path.realpath(path)

    # Create the directory
    os.makedirs(realpath, exist_ok=True)

    # Create the README.md
    create_readme(project, realpath)

    # Create the files
    create_files(project, realpath)

    # Save project info
    save_project_info(project, realpath)


def create_readme(project: upsilon_workshop_client.api.project.Project,
                  path: str) -> None:
    """Create the README.md file."""
    readme = f"# {project.name}\n\n"

    readme += f"{project.description}\n"

    # Save the file
    with open(f"{path}/README.md", "w", encoding="utf-8") as f:
        f.write(readme)


def create_files(project: upsilon_workshop_client.api.project.Project,
                 path: str) -> None:
    """Create the files."""
    # Create the files
    for file in project.files:
        with open(f"{path}/{file['name']}", "w", encoding="utf-8") as f:
            f.write(file["content"])


def save_project_info(project: upsilon_workshop_client.api.project.Project,
                      path: str) -> None:
    """Save the URL to the project."""
    # Generate the JSON
    project_info = {
        "url": project.url,
        "language": project.language,
        "version": project.version,
        "licence": project.licence,
        "compatibility": project.compatibility,
        "file_version": 1  # May be used in the future to handle compatibility
    }
    with open(f"{path}/.project_info.json", "w", encoding="utf-8") as f:
        # Save the JSON
        f.write(json.dumps(project_info, indent=4))
