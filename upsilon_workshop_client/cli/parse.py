"""Client for the Upsilon Workshop - Main Argument parser."""
# Standard Library
import logging
import sys

# Import Rich logger if available
try:
    from rich.logging import RichHandler

    has_rich_logger = True
except ImportError:
    has_rich_logger = False

# Internal
import upsilon_workshop_client.commands
import upsilon_workshop_client.cli.parser

logger = logging.getLogger(__name__)


def parse_args() -> upsilon_workshop_client.commands.base_command.Command:
    """Parse the arguments."""
    logger.debug("Parsing arguments...")

    # Create the parser
    parser = upsilon_workshop_client.cli.parser.create_parser()

    # Parse the arguments
    args = parser.parse_args()

    # Parse verbosity
    logging.basicConfig(
        format="%(message)s",
        level=logging.WARNING if args.verbose == 0
        else logging.INFO if args.verbose == 1
        else logging.DEBUG,
        handlers=[RichHandler()] if has_rich_logger else None,
    )

    # Instantiate the appropriate command
    if args.command == "clone":
        command = upsilon_workshop_client.commands.clone.Clone(args)
    elif args.command == "push":
        command = upsilon_workshop_client.commands.push.Push(args)
    else:
        # No command specified
        logger.error("No command specified.")
        parser.print_help()
        sys.exit(1)

    return command
