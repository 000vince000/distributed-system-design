from .base_step import BaseStep

class OptimizationStep(BaseStep):
    def execute(self, design_data):
        """Add design optimizations."""
        self.console.print("\n[bold]Step 5: Design Optimization[/bold]")
        design_data["optimizations"] = self._get_multi_line_input(
            "Enter optimizations (one per line, x to finish):",
            "x"
        )
        return design_data 