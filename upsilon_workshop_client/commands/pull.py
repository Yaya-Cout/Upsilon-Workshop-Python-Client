"""Client for the Upsilon Workshop - Pull command."""
# Standard Library
import logging

# Internal
import upsilon_workshop_client.utils.pull
from . import base_command

logger = logging.getLogger(__name__)


class Pull(base_command.Command):
    """Pull a project."""

    def __init__(self, args):
        """Initialize the class."""
        logger.debug("Initializing pull command...")
        self.args = args
        self.path: str = self.args.path

    def run(self):
        """Run the command."""
        # Check the arguments
        self.check_args()

        # Pull the project
        upsilon_workshop_client.utils.pull.pull(self.path)

    def check_args(self):
        """Check that required arguments are present."""
        return True
