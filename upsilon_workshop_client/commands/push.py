"""Client for the Upsilon Workshop - Push command."""
# Standard Library
import logging

# Internal
from . import base_command
import upsilon_workshop_client.utils.push

logger = logging.getLogger(__name__)


class Push(base_command.Command):
    """Push a project."""

    name = "push"

    def __init__(self, args):
        """Initialize the class."""
        logger.debug("Initializing push command...")
        self.args = args
        self.path: str = self.args.path

    def run(self):
        """Run the command."""
        # Check the arguments
        self.check_args()

        # Push the project
        upsilon_workshop_client.utils.push.push(self.path)

    def check_args(self):
        """Check that required arguments are present."""
        return True
