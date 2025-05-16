from .base_step import BaseStep

class RequirementsStep(BaseStep):
    def execute(self, design_data):
        """Gather functional and non-functional requirements."""
        self.navigation_helper.display_step_header(1)
        
        self.console.print("\n[bold]Functional Requirements:[/bold]")
        design_data["requirements"]["functional"] = self.input_helper.get_multi_line_input(
            "Enter functional requirements (one per line, x to finish):"
        )

        self.console.print("\n[bold]Non-functional Requirements:[/bold]")
        design_data["requirements"]["nonfunctional"] = self.input_helper.get_multi_line_input(
            "Enter non-functional requirements (one per line, x to finish):"
        )
        
        return design_data 