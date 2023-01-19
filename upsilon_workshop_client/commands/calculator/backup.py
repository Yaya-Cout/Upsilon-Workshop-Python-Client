"""Client for the Upsilon Workshop - Calculator backup command."""
import logging
import asyncio

from upsilon_workshop_client.commands import base_command
import upsilon_workshop_client.utils.calculator.backup

logger = logging.getLogger(__name__)


class Backup(base_command.Command):
    """Run a command."""

    name = "backup"

    def __init__(self, args) -> None:
        """Initialize the class."""
        logger.debug("Initializing %s command...", self.name)
        self.args = args
        self.directory = self.args.directory

    def run(self) -> None:
        """Run the command."""
        logger.info("Running %s command...", self.name)
        # Check the arguments
        self.check_args()

        # Backup the scripts
        asyncio.run(upsilon_workshop_client.utils.calculator.backup.backup(
            self.directory))

    def check_args(self) -> bool:
        """Check that required arguments are present."""
        return True
