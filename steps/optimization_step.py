from .base_step import BaseStep

class OptimizationStep(BaseStep):
    def execute(self, design_data):
        """Add design optimizations."""
        self.console.print("\n[bold]Step 5: Design Optimization[/bold]")
        
        # Get non-functional requirements
        nonfunctional_reqs = design_data["requirements"]["nonfunctional"]
        if not nonfunctional_reqs:
            self.console.print("[yellow]No non-functional requirements defined. Please define requirements first.[/yellow]")
            return design_data
            
        # Display non-functional requirements for selection
        self.console.print("\n[bold]Select non-functional requirements to optimize for:[/bold]")
        for i, req in enumerate(nonfunctional_reqs, 1):
            self.console.print(f"{i}. {req}")
        self.console.print(f"{len(nonfunctional_reqs) + 1}. All requirements")
        
        # Get user selection
        choices = [str(i) for i in range(1, len(nonfunctional_reqs) + 2)]
        selected = self.prompt.ask(
            "Select requirements to optimize for (comma-separated numbers):",
            choices=choices
        )
        
        # Parse selected requirements
        selected_indices = [int(x.strip()) for x in selected.split(",")]
        selected_reqs = []
        if len(nonfunctional_reqs) + 1 in selected_indices:
            selected_reqs = nonfunctional_reqs
        else:
            selected_reqs = [nonfunctional_reqs[i-1] for i in selected_indices if 1 <= i <= len(nonfunctional_reqs)]
        
        # Get optimizations for each selected requirement
        optimizations = []
        for req in selected_reqs:
            self.console.print(f"\n[bold]Enter optimizations for: {req}[/bold]")
            req_optimizations = self._get_multi_line_input(
                "Enter optimizations (one per line, x to finish):",
                "x"
            )
            optimizations.extend([f"{req}: {opt}" for opt in req_optimizations])
        
        design_data["optimizations"] = optimizations
        return design_data 