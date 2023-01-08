"""Client for the Upsilon Workshop - CLI entry point."""
# Standard Library
import logging

# Internal
import upsilon_workshop_client

logger = logging.getLogger(__name__)


def main():
    """Entry point for the CLI."""
    logger.debug("Starting...")

    # Parse the arguments
    command = upsilon_workshop_client.cli.parse.parse_args()

    logger.debug("Running command...")

    # Run the command
    command.run()


if __name__ == "__main__":
    main()
