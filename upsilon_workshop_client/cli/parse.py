"""Client for the Upsilon Workshop - Main Argument parser."""
# Standard Library
import logging

import typer

# Import Rich logger if available
try:
    from rich.logging import RichHandler

    HAS_RICH_LOGGER = True
except ImportError:
    HAS_RICH_LOGGER = False

from . import workshop, calculator, simulator

logger = logging.getLogger(__name__)


app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})
app.add_typer(
    workshop.app,
    name="workshop",
    help="Workshop interaction commands"
)
app.add_typer(
    calculator.app,
    name="calculator",
    help="Calculator management commands"
)
app.add_typer(
    simulator.app,
    name="simulator",
    help="Simulator management commands"
)


@app.callback()
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output.",
    ),
    url: str = typer.Option(
        "https://django-cdqivkhudi9mmk5gqgb0.apps.playground.napptive.dev/",
        help="The URL of the Upsilon Workshop server.",
    ),
) -> None:
    """Upsilon CLI."""
    if verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler()] if HAS_RICH_LOGGER
            else [logging.StreamHandler()],
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler()] if HAS_RICH_LOGGER
            else [logging.StreamHandler()],
        )

    # Remove the first and last slash from the url if present
    url = url.strip("/")

    ctx.obj = {"url": url, "verbose": verbose}


def parse_args() -> None:
    """Parse the arguments."""
    logger.debug("Parsing arguments...")

    # Parse the arguments
    app()
