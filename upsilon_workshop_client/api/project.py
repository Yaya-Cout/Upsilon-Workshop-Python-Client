"""Client for the Upsilon Workshop - Project API."""
# Standard Library
import logging
import requests
import datetime

logger = logging.getLogger(__name__)


class Project:
    """Project object."""

    def __init__(self, project: dict[
            str, str | int | list[str] | list[dict[str, str]]
    ]) -> None:
        """Initialize the class."""
        logger.debug("Initializing project object...")
        self.project = project

        self.parse()

    def parse(self):
        """Parse the project."""
        logger.debug("Parsing project...")

        # Add url to the project
        # self.url: str = self.project["url"]
        # Remove the server url from the project url (keep only the /scripts/UUID/)
        self.url: str = "/scripts/" + self.project["url"].split("/scripts/")[-1]


        # Add name to the project
        self.name: str = self.project["name"]

        # Add creation and modification dates to the project
        self.created = datetime.datetime.fromisoformat(
            self.project["created"].replace("Z", "+00:00")
        )
        self.modified = datetime.datetime.fromisoformat(
            self.project["modified"].replace("Z", "+00:00")
        )

        # Add language to the project
        self.language: str = self.project["language"]

        # Add version to the project
        self.version: str = self.project["version"]

        # Add short description to the project
        self.short_description: str = self.project["short_description"]

        # Add long description to the project
        self.long_description: str = self.project["long_description"]

        # Add ratings to the project
        self.ratings: float = self.project["ratings"]

        # Add author to the project
        self.author: str = self.project["author"].split("/")[-2]

        # TODO: Collaborators

        # Add files to the project
        self.files: list[dict[str, str]] = self.project["files"]

        # Add license to the project
        self.licence: str = self.project["licence"]

        # Add compatibility to the project
        self.compatibility: str = self.project["compatibility"]

        # Add views to the project
        self.views: int = self.project["views"]


def get_project(project_name: str) -> Project:
    """Get a project."""
    logger.debug("Getting project %s...", project_name)

    # Request the server
    response = requests.get(
        project_name,
        timeout=5,
    )

    # Check the response
    if response.status_code != 200:
        logger.error(
            "Failed to get project %s: %s (status code %s)",
            project_name,
            response.text,
            response.status_code,
        )
        raise ValueError(
            f"Failed to get project {project_name}: {response.text} "
            "(status code {response.status_code})"
        )

    # Parse the response into a dict (JSON)
    project_dict = response.json()

    # Turn the project into a Project object
    return Project(project_dict)
