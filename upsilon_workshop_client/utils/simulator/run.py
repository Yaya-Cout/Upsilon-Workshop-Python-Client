"""Client for the Upsilon Workshop - Simulator Run."""
import logging
import os
import subprocess
from typing import Optional

import requests

logger = logging.getLogger(__name__)


def run(project: Optional[str], firmware: str):
    """Run a project."""
    if project is None:
        logger.log(logging.DEBUG, "Running %s simulator", firmware)
    else:
        logger.log(logging.DEBUG, "Running %s simulator for project %s",
                   firmware, project)

    path = f"{firmware}.{'exe' if os.name == 'nt' else 'bin'}"

    # Download the simulator if path does not exist
    if not os.path.exists(path):
        logger.debug("Simulator not found, downloading it")
        download_simulator(firmware, path)
    else:
        logger.debug("Simulator found, skipping download")

    # Set the path to the simulator real path
    path = os.path.realpath(path)

    # Generate the command arguments to run the simulator
    command_args = generate_command_args(project)

    # Run the simulator
    subprocess.run([path, *command_args], check=True)


def generate_command_args(project: Optional[str]) -> list[str]:
    """Generate the command arguments to run the simulator."""
    logger.debug("Generating command arguments")

    # Generate the command arguments to run the simulator
    if project is None:
        # Run the simulator without a project
        command_args = []
    elif os.path.isdir(project):
        logger.error("Running a directory is not supported yet")
        raise NotImplementedError
    else:
        # Ensure the project is a file
        if not os.path.isfile(project):
            logger.error("Project %s is not a file", project)
            raise FileNotFoundError(
                "Importing a directory is not supported yet")

        # Read the content of the file
        with open(project, 'r', encoding='utf-8') as file:
            content = file.read()

        # Get the file name (without the directory)
        project = os.path.basename(project)

        # Generate the command arguments
        command_args = [
            "--code-script",
            f"{project}:{content}",
            "--code-lock-on-console",
            "--volatile"
        ]

    return command_args


def download_simulator(firmware: str, path: str):
    """Download the simulator."""
    logger.debug("Downloading %s simulator", firmware)

    # Download the simulator that matches the firmware
    if firmware == "upsilon":
        # Download the Upsilon simulator
        download_simulator_upsilon(path)
    else:
        logger.error("Unknown simulator %s", firmware)
        raise NotImplementedError(f"Unknown simulator {firmware}")


def download_simulator_upsilon(path: str):
    """Download the Upsilon simulator."""
    bucket_name = 'upsilon-binfiles.appspot.com'

    # Generate the file name
    file_name = f"dev%2Fsimulator%2Fepsilon.{path.split('.')[-1]}"

    # Get the download token.
    token = get_token(bucket_name, file_name)

    # Generate the URL of the file.
    url = f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/" + \
          f"{file_name}?alt=media&token={token}"

    # Download the file.
    response = requests.get(url, timeout=30)

    # Save the file.
    with open(path, 'w+b') as file:
        file.write(response.content)

    # Make the file executable.
    os.chmod(path, 0o755)


def get_token(bucket_name: str, file_name: str) -> str:
    """Get a download token from a Firebase bucket."""
    # Generate the URL of the file.
    url = "https://firebasestorage.googleapis.com/v0/b/" + \
        f"{bucket_name}/o/{file_name}"

    # Download the file.
    response = requests.get(url, timeout=30)

    # Parse the response as JSON.
    json = response.json()

    return json['downloadTokens']
