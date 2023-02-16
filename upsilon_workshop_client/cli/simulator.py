"""Client for the Upsilon Workshop - Calculator Argument parser."""
# Standard Library
import logging
from typing import Optional

# Third-party
import typer

# Internal modules
import upsilon_workshop_client.utils.simulator as simulator_utils


# Initialize logger
logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def run(
    project: Optional[str] = typer.Argument(
        None,
        help="Project to import into the simulator.",
    ),
    firmware: str = typer.Option(
        "upsilon",
        "--firmware",
        "-f",
        help="Simulator firmware to use.",
    ),
):
    """Run a simulator."""
    logger.info("Starting simulator")

    simulator_utils.run.run(project, firmware)


if __name__ == "__main__":
    app()
