"""Client for the Upsilon Workshop - Base command class."""
import logging

logger = logging.getLogger(__name__)


class Command:
    """Run a command."""

    name = None

    def __init__(self, args) -> None:
        """Initialize the class."""
        if not self.name:
            raise NotImplementedError("Command name not specified.")

        logger.debug("Initializing %s command...", self.name)
        self.args = args

    def run(self) -> None:
        """Run the command."""
        logger.info("Running %s command...", self.name)

    def check_args(self) -> bool:
        """Check that required arguments are present."""
        return True
