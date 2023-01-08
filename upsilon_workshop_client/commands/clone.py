"""Client for the Upsilon Workshop - Clone command."""
# Standard Library
import logging

# Internal
from . import base_command
import upsilon_workshop_client.utils.clone

logger = logging.getLogger(__name__)


class Clone(base_command.Command):
    """Clone a project."""

    def __init__(self, args):
        """Initialize the class."""
        logger.debug("Initializing clone command...")
        self.args = args
        self.project: str = self.args.project
        self.path: str = self.args.path

    def run(self):
        """Run the command."""
        # Check the arguments
        self.check_args()

        # Clone the project
        upsilon_workshop_client.utils.clone.clone(self.project, self.path)


    def check_args(self):
        """Check that required arguments are present."""
        if not self.project:
            raise ValueError("No project specified.")
        return True
