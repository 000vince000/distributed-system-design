from .base_step import BaseStep

class EdgeCasesStep(BaseStep):
    def __init__(self, console=None):
        super().__init__(console)
        self.small_scale_failures = {
            "1": "Memory leak",
            "2": "Cache misses",
            "3": "Message loss",
            "4": "Race condition",
            "5": "Deadlock",
            "6": "Cascading failure"
        }
        self.large_scale_failures = {
            "1": "3P API down",
            "2": "Service overwhelmed",
            "3": "DDoS",
            "4": "Node down",
            "5": "Cluster down",
            "6": "Deployment failure"
        }

    def _get_failure_mitigations(self, failure_type: str, failures: dict):
        """Get user's selected failures and their mitigation strategies."""
        selected_failures = []
        available_failures = failures.copy()
        
        while available_failures:
            # Show available failures
            self.console.print(f"\n[bold]Select {failure_type} failures to address:[/bold]")
            for key, value in available_failures.items():
                self.console.print(f"{key}. {value}")
            self.console.print("x. Done")
            
            # Get user's selection
            choices = list(available_failures.keys()) + ['x']
            selected = self.prompt.ask(
                "Select a failure (or 'x' to finish):",
                choices=choices
            )
            
            if selected == 'x':
                break
                
            if selected in available_failures:
                failure = available_failures[selected]
                self.console.print(f"\n[bold]Mitigation for {failure}:[/bold]")
                mitigation = self._get_multi_line_input(
                    "Enter prevention/mitigation mechanisms (one per line, x to finish):",
                    "x"
                )
                selected_failures.append({
                    "failure": failure,
                    "mitigation": mitigation
                })
                # Remove the selected failure from available options
                del available_failures[selected]
        
        return selected_failures

    def execute(self, design_data):
        """Identify edge cases and failure scenarios."""
        # Initialize edge cases structure if not exists
        if "edge_cases" not in design_data:
            design_data["edge_cases"] = {
                "edge_cases": [],
                "small_scale": [],
                "large_scale": []
            }
        
        # Get general edge cases
        self.console.print("\n[bold]Edge Cases[/bold]")
        design_data["edge_cases"]["edge_cases"] = self._get_multi_line_input(
            "Enter general edge cases (one per line, x to finish):",
            "x"
        )

        # Get small scale failures and their mitigations
        self.console.print("\n[bold]Small Scale Failures[/bold]")
        design_data["edge_cases"]["small_scale"] = self._get_failure_mitigations(
            "small scale",
            self.small_scale_failures
        )

        # Get large scale failures and their mitigations
        self.console.print("\n[bold]Large Scale Failures[/bold]")
        design_data["edge_cases"]["large_scale"] = self._get_failure_mitigations(
            "large scale",
            self.large_scale_failures
        )
        
        # Display summary
        if any([
            design_data["edge_cases"]["edge_cases"],
            design_data["edge_cases"]["small_scale"],
            design_data["edge_cases"]["large_scale"]
        ]):
            self.console.print("\n[bold]Failure Handling Summary:[/bold]")
            
            if design_data["edge_cases"]["edge_cases"]:
                self.console.print("\n[bold]Edge Cases:[/bold]")
                for edge_case in design_data["edge_cases"]["edge_cases"]:
                    self.console.print(f"  - {edge_case}")
            
            if design_data["edge_cases"]["small_scale"]:
                self.console.print("\n[bold]Small Scale Failures:[/bold]")
                for failure in design_data["edge_cases"]["small_scale"]:
                    self.console.print(f"\n{failure['failure']}:")
                    for mitigation in failure['mitigation']:
                        self.console.print(f"  - {mitigation}")
            
            if design_data["edge_cases"]["large_scale"]:
                self.console.print("\n[bold]Large Scale Failures:[/bold]")
                for failure in design_data["edge_cases"]["large_scale"]:
                    self.console.print(f"\n{failure['failure']}:")
                    for mitigation in failure['mitigation']:
                        self.console.print(f"  - {mitigation}")
        
        return design_data 