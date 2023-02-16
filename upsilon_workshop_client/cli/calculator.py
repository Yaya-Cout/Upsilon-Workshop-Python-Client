"""Client for the Upsilon Workshop - Calculator Argument parser."""
# Standard Library
import logging
import asyncio

# Third-party
import typer

# Internal modules
import upsilon_workshop_client.utils.calculator as calculator_utils


# Initialize logger
logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def backup(
    destination: str = typer.Argument("backup"),
):
    """Backup a project."""
    logger.debug("Backing up calculator to %s", destination)

    asyncio.run(calculator_utils.backup.backup(destination))


@app.command()
def upload(
    source: str = typer.Argument("backup"),
):
    """Upload a project."""
    logger.debug("Uploading calculator from %s", source)

    asyncio.run(calculator_utils.upload.upload(source))


if __name__ == "__main__":
    app()
