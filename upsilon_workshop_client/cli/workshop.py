"""Client for the Upsilon Workshop - Workshop Argument parser."""
# Standard library
import logging

# Third-party
import typer

# Internal modules
import upsilon_workshop_client.utils as utils


# Initialize logger
logger = logging.getLogger(__name__)

# Initialize typer app
app = typer.Typer()


@app.command()
def clone(
    ctx: typer.Context,
    project: str,
    destination: str = typer.Argument("."),
):
    """Clone a project."""
    # Remove the first and last slash from the project if present
    project = project.strip("/")

    # If the project is just the UUID, we need to add the /scripts/ prefix
    if not project.startswith("/scripts/") and\
            not project.startswith("scripts/"):
        project = f"/scripts/{project}"

    # If the project is /scripts/UUID, we need to add the url
    if project.startswith("/scripts/") or project.startswith("scripts/"):
        # Add the url
        project = ctx.obj["url"] + project

    # Add a trailing slash to the project if not present
    if not project.endswith("/"):
        project += "/"

    logger.debug("Cloning project %s to %s", project, destination)

    utils.clone.clone(project, destination)


@app.command()
def push(
    project: str = typer.Argument(".")
):
    """Push a project."""
    logger.debug("Pushing project %s", project)

    utils.push.push(project)


@app.command()
def pull(
    project: str,
):
    """Pull a project."""
    logger.debug("Pulling project %s", project)

    utils.pull.pull(project)


@app.command()
def init(
    ctx: typer.Context,
    path: str = typer.Argument("."),
):
    """Init a project."""
    logger.debug("Initializing project %s", path)

    utils.init.init(path, ctx.obj["url"])


@app.command()
def search(
    ctx: typer.Context,
    keywords: list[str],
):
    """Search a project."""
    logger.debug("Searching project %s", keywords)

    utils.search.search(keywords, ctx.obj["url"])


if __name__ == "__main__":
    app()
