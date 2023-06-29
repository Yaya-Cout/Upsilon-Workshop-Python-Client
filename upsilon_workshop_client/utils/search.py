"""Client for the Upsilon Workshop - Project searching handler."""
# Standard Library
import logging
import rich

# Internal
import upsilon_workshop_client.api.search

logger = logging.getLogger(__name__)


def search(keywords: list[str], url: str) -> None:
    """Search a project."""
    logger.info("Searching %s.", keywords)

    # Search the project
    results = upsilon_workshop_client.api.search.search_project(
        keywords, url)

    # Display the results
    display_results(results)


def display_results(results:
        list[upsilon_workshop_client.api.project.Project]) -> None:
    """Display the results."""
    logger.debug("Displaying results...")

    # Create the table (align on the middle)
    table = rich.table.Table("Name", "Author", "Language", "Version",
                             "Description", "URL", title="Results",
                             box=rich.box.HORIZONTALS)


    for result in results:
        table.add_row(
            result.name,
            result.author,
            result.language,
            result.version,
            result.short_description,
            result.url,
        )

    # If there are no results, display a message
    if not results:
        rich.print("No results found.")
    else:
        rich.print(table)
