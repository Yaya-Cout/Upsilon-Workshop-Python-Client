"""Client for the Upsilon Workshop - Project Search API."""
# Standard Library
import logging
import requests

# Internal
from . import project

logger = logging.getLogger(__name__)


def search_project(keywords: list[str], url: str) -> list[project.Project]:
    """Search a project."""
    logger.debug("Searching %s...", keywords)

    # Construct the URL
    search_url = f"{url}/scripts/?search="

    # Add the keywords to the URL
    for keyword in keywords:
        search_url += f"{keyword}+"

    # Remove the last +
    search_url = search_url[:-1]

    # Get the response
    response = requests.get(search_url, timeout=10)

    # Check the response
    if response.status_code != 200:
        logger.error(
            "Failed to search %s: %s (status code %s)",
            keywords,
            response.text,
            response.status_code,
        )
        raise ValueError(
            f"Failed to search {keywords}: {response.text} "
            f"(status code {response.status_code})",
        )

    return [
        project.Project(result) for result in response.json()["results"]
    ]
