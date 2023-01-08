"""Client for the Upsilon Workshop - Argument parser creation."""
import argparse
import logging

logger = logging.getLogger(__name__)


def add_verbosity(parser: argparse.ArgumentParser) -> None:
    """Add verbosity arguments to the parser."""
    logger.debug("Adding verbosity arguments...")
    # Verbose mode (multiple -v for more verbosity)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase output verbosity",
    )


def add_clone(subparser: argparse._SubParsersAction) -> None:
    """Add clone arguments to the parser."""
    logger.debug("Adding clone command...")
    # Clone a project (upsilon_workshop_client clone <project>)
    clone_parser = subparser.add_parser(
        "clone",
        help="clone a project",
    )

    # Add the arguments
    # Project to clone
    clone_parser.add_argument(
        "project",
        help="project to clone",
    )

    # Destination path (default: ., not required)
    clone_parser.add_argument(
        "path",
        help="destination path",
        default=".",
        nargs="?",
    )


def add_push(subparser: argparse._SubParsersAction) -> None:
    """Add push arguments to the parser."""
    logger.debug("Adding push command...")
    # Push a project (upsilon_workshop_client push <project>)
    push_parser = subparser.add_parser(
        "push",
        help="push a project",
    )

    # Add the arguments
    # Path of project to push
    push_parser.add_argument(
        "path",
        help="path of project to push",
        default=".",
        nargs="?",
    )


def add_commands(parser: argparse.ArgumentParser) -> None:
    """Add commands to the parser."""
    logger.debug("Adding commands...")

    subparsers = parser.add_subparsers(
        dest="command",
    )

    # Add the commands
    add_clone(subparsers)
    add_push(subparsers)


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    logger.debug("Creating argument parser...")

    # Create the parser
    parser = argparse.ArgumentParser(
        description="Upsilon Workshop CLI."
    )

    # Add the arguments
    add_verbosity(parser)

    # Add the commands
    add_commands(parser)

    return parser
