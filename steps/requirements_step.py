from .base_step import BaseStep

class RequirementsStep(BaseStep):
    def execute(self, design_data):
        """Gather functional and non-functional requirements."""
        self.console.print("\n[bold]Step 1: Requirement Gathering[/bold]")
        
        self.console.print("\n[bold]Functional Requirements:[/bold]")
        design_data["requirements"]["functional"] = self._get_multi_line_input(
            "Enter functional requirements (one per line, x to finish):",
            "x"
        )

        self.console.print("\n[bold]Non-functional Requirements:[/bold]")
        design_data["requirements"]["nonfunctional"] = self._get_multi_line_input(
            "Enter non-functional requirements (one per line, x to finish):",
            "x"
        )
        
        return design_data 