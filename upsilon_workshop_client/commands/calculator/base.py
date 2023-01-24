"""Client for the Upsilon Workshop - Calculator command handler."""
import logging

import upsilon_workshop_client.commands.calculator
from upsilon_workshop_client.commands import base_command

logger = logging.getLogger(__name__)


class Calculator(base_command.Command):
    """Handle the calculator command."""

    name = "calculator"

    def __init__(self, args) -> None:
        """Initialize the class."""
        logger.debug("Initializing %s command...", self.name)
        self.args = args
        self.calculator_command: str = self.args.calculator_command

    def run(self) -> None:
        """Run the command."""
        logger.info("Running %s command...", self.name)
        self.check_args()

        # Get the subcommand
        if self.calculator_command == "backup":
            calculator_command = upsilon_workshop_client.commands.calculator.\
                    backup.Backup(self.args)
        elif self.calculator_command == "upload":
            calculator_command = upsilon_workshop_client.commands.calculator.\
                    upload.Upload(self.args)
        else:
            raise NotImplementedError(
                f"Calculator command '{self.calculator_command}' not "
                "implemented."
            )

        # Run the subcommand
        calculator_command.run()

    def check_args(self) -> bool:
        """Check that required arguments are present."""
        if not self.calculator_command:
            raise ValueError("No calculator subcommand specified.")
        return True
