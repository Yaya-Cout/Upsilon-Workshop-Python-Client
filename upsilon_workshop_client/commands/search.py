"""Client for the Upsilon Workshop - Search command."""
# Standard Library
import logging

# Internal
import upsilon_workshop_client.utils.search
from . import base_command

logger = logging.getLogger(__name__)


class Search(base_command.Command):
    """Search a project."""

    def __init__(self, args):
        """Initialize the class."""
        logger.debug("Initializing searc command...")
        self.args = args
        self.keywords: list[str] = self.args.keywords
        self.url: str = self.args.url

    def run(self):
        """Run the command."""
        # Check the arguments
        self.check_args()

        # Search the project
        upsilon_workshop_client.utils.search.search(self.keywords, self.url)

    def check_args(self):
        """Check that required arguments are present."""
        return True
