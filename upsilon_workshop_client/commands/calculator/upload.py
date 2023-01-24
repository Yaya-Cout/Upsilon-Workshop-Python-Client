"""Client for the Upsilon Workshop - Calculator upload command."""
import logging
import asyncio

from upsilon_workshop_client.commands import base_command
import upsilon_workshop_client.utils.calculator.upload

logger = logging.getLogger(__name__)


class Upload(base_command.Command):
    """Upload a file."""

    name = "backup"

    def __init__(self, args) -> None:
        """Initialize the class."""
        logger.debug("Initializing %s command...", self.name)
        self.args = args
        self.filename = self.args.filename

    def run(self) -> None:
        """Run the command."""
        logger.info("Running %s command...", self.name)
        # Check the arguments
        self.check_args()

        # Backup the scripts
        asyncio.run(upsilon_workshop_client.utils.calculator.upload.upload(
            self.filename))

    def check_args(self) -> bool:
        """Check that required arguments are present."""
        return True
