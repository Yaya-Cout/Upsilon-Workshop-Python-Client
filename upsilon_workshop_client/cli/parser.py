"""Client for the Upsilon Workshop - Argument parser creation."""
import argparse
import logging

logger = logging.getLogger(__name__)


def add_global(parser: argparse.ArgumentParser) -> None:
    """Add global arguments to the parser."""
    logger.debug("Adding global arguments...")
    # Verbose mode (multiple -v for more verbosity)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase output verbosity",
    )

    # Url of the server
    parser.add_argument(
        "--url",
        help="url of the server",
        default="http://127.0.0.1:8000/",
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
    push_parser: argparse.ArgumentParser = subparser.add_parser(
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


def add_init(subparser: argparse._SubParsersAction) -> None:
    """Add init arguments to the parser."""
    logger.debug("Adding init command...")
    # Init a project (upsilon_workshop_client init <project>)
    init_parser: argparse.ArgumentParser = subparser.add_parser(
        "init",
        help="init a project",
    )

    # Add the arguments
    # Path of project to init
    init_parser.add_argument(
        "path",
        help="path of project to init",
        default=".",
        nargs="?",
    )


def add_pull(subparser: argparse._SubParsersAction) -> None:
    """Add pull arguments to the parser."""
    logger.debug("Adding pull command...")
    # Pull a project (upsilon_workshop_client pull <project>)
    pull_parser: argparse.ArgumentParser = subparser.add_parser(
        "pull",
        help="pull a project",
    )

    # Add the arguments
    # Path of project to pull
    pull_parser.add_argument(
        "path",
        help="path of project to pull",
        default=".",
        nargs="?",
    )

def add_search(subparser: argparse._SubParsersAction) -> None:
    """Add search arguments to the parser."""
    logger.debug("Adding search command...")
    # Search a project (upsilon_workshop_client search <project>)
    search_parser: argparse.ArgumentParser = subparser.add_parser(
        "search",
        help="search a project",
    )

    # Add the arguments
    # Project to search
    search_parser.add_argument(
        "keywords",
        help="keywords to search",
        nargs="+",
    )


def add_calculator(subparser: argparse._SubParsersAction) -> None:
    """Add calculator arguments to the parser."""
    logger.debug("Adding calculator command...")
    # Calculator (upsilon_workshop_client calculator <command> <expression>)
    # Create a "subsubparser" for the calculator
    calculator_parser: argparse.ArgumentParser = subparser.add_parser(
        "calculator",
        help="calculator subcommands",
    )

    # Add the calculator commands
    # Test command (upsilon_workshop_client calculator test <expression>)
    test_parser = calculator_parser.add_subparsers(
        dest="calculator_command",
        required=True,
    )

    # Add the arguments
    # Backup command (upsilon_workshop_client calculator backup <expression>)
    test_parser.add_parser(
        "backup",
        help="backup all the files"
    ).add_argument(
        "directory",
        help="destination directory",
        default="backup",
        nargs="?",
    )


def add_commands(parser: argparse.ArgumentParser) -> None:
    """Add commands to the parser."""
    logger.debug("Adding commands...")

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # Add the commands
    add_clone(subparsers)
    add_push(subparsers)
    add_pull(subparsers)
    add_init(subparsers)
    add_search(subparsers)
    add_calculator(subparsers)


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    logger.debug("Creating argument parser...")

    # Create the parser
    parser = argparse.ArgumentParser(
        description="Upsilon Workshop CLI."
    )

    # Add the arguments
    add_global(parser)

    # Add the commands
    add_commands(parser)

    return parser
