from .base_step import BaseStep
from .helpers import InputHelper, DisplayHelper, StepNavigationHelper

class RequirementsStep(BaseStep):
    def __init__(self, console=None):
        super().__init__(console)
        self.input_helper = InputHelper(self.console, self.prompt)
        self.display_helper = DisplayHelper(self.console)
        self.nav_helper = StepNavigationHelper(self.console, self.prompt)

    def execute(self, design_data):
        """Gather functional and non-functional requirements."""
        self.nav_helper.display_step_header(1)
        
        self.console.print("\n[bold]Functional Requirements:[/bold]")
        design_data["requirements"]["functional"] = self.input_helper.get_multi_line_input(
            "Enter functional requirements (one per line, x to finish):",
            "x"
        )

        self.console.print("\n[bold]Non-functional Requirements:[/bold]")
        design_data["requirements"]["nonfunctional"] = self.input_helper.get_multi_line_input(
            "Enter non-functional requirements (one per line, x to finish):",
            "x"
        )
        
        return design_data 