"""Client for the Upsilon Workshop - Init command."""
# Standard Library
import logging

# Internal
from . import base_command
import upsilon_workshop_client.utils.init

logger = logging.getLogger(__name__)


class Init(base_command.Command):
    """Init a project."""

    def __init__(self, args):
        """Initialize the class."""
        logger.debug("Initializing init command...")
        self.args = args
        self.path: str = self.args.path
        self.url: str = self.args.url

    def run(self):
        """Run the command."""
        # Check the arguments
        self.check_args()

        # Init the project
        upsilon_workshop_client.utils.init.init(self.path, self.url)

    def check_args(self):
        """Check that required arguments are present."""
        return True
