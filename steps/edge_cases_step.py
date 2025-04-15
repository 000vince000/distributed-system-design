from .base_step import BaseStep

class EdgeCasesStep(BaseStep):
    def execute(self, design_data):
        """Identify edge cases."""
        self.console.print("\n[bold]Step 6: Edge Cases[/bold]")
        
        self.console.print("\n[bold]Small Edge Cases:[/bold]")
        design_data["edge_cases"]["small"] = self._get_multi_line_input(
            "Enter small edge cases (one per line, END to finish):",
            "END"
        )

        self.console.print("\n[bold]Big Edge Cases:[/bold]")
        design_data["edge_cases"]["big"] = self._get_multi_line_input(
            "Enter big edge cases (one per line, END to finish):",
            "END"
        )
        return design_data 