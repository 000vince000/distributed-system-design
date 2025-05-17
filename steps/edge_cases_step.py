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
        """Get user's selected failures and their prevention/mitigation strategies."""
        selected_failures = []
        available_failures = failures.copy()
        
        while available_failures:
            # Show available failures
            self.console.print(f"\n[bold]Select {failure_type} failures to address:[/bold]")
            self.display_helper.display_list(available_failures.values(), enumerate_items=True)
            self.console.print("x. Done")
            
            # Get user's selection
            choices = list(available_failures.keys()) + [self.input_helper.SKIP_CHOICE]
            selected = self.input_helper.get_choice(
                "Select a failure",
                choices=choices
            )
            
            if selected == self.input_helper.SKIP_CHOICE:
                break
                
            if selected in available_failures:
                failure = available_failures[selected]
                self.console.print(f"\n[bold]Failure:[/bold] {failure}")
                prevention = []
                mitigation = []
                
                add_prevention = self.input_helper.get_choice(
                    "Add prevention strategies?",
                    choices=["y", "n"],
                    default="y"
                )
                if add_prevention == "y":
                    prevention = self.input_helper.get_multi_line_input(
                        "Enter prevention strategies (one per line, x to finish):"
                    )
                    
                add_mitigation = self.input_helper.get_choice(
                    "Add mitigation strategies?",
                    choices=["y", "n"],
                    default="y"
                )
                if add_mitigation == "y":
                    mitigation = self.input_helper.get_multi_line_input(
                        "Enter mitigation strategies (one per line, x to finish):"
                    )
                    
                selected_failures.append({
                    "failure": failure,
                    "prevention": prevention,
                    "mitigation": mitigation
                })
                # Remove the selected failure from available options
                del available_failures[selected]
        
        return selected_failures

    def execute(self, design_data):
        """Identify edge cases and failure scenarios."""
        self.navigation_helper.display_step_header(6)
        
        # Initialize edge cases structure if not exists
        if "edge_cases" not in design_data:
            design_data["edge_cases"] = {
                "edge_cases": [],
                "small_scale": [],
                "large_scale": []
            }
        
        # Get general edge cases
        edge_cases = self.input_helper.get_multi_line_input(
            "Enter general edge cases (one per line, x to finish):"
        )
        edge_cases_with_strategies = []
        for edge_case in edge_cases:
            self.console.print(f"\n[bold]Edge Case:[/bold] {edge_case}")
            prevention = []
            mitigation = []
            
            add_prevention = self.input_helper.get_choice(
                "Add prevention strategies?",
                choices=["y", "n"],
                default="y"
            )
            if add_prevention == "y":
                prevention = self.input_helper.get_multi_line_input(
                    "Enter prevention strategies (one per line, x to finish):"
                )
                
            add_mitigation = self.input_helper.get_choice(
                "Add mitigation strategies?",
                choices=["y", "n"],
                default="y"
            )
            if add_mitigation == "y":
                mitigation = self.input_helper.get_multi_line_input(
                    "Enter mitigation strategies (one per line, x to finish):"
                )
                
            edge_cases_with_strategies.append({
                "edge_case": edge_case,
                "prevention": prevention,
                "mitigation": mitigation
            })
        design_data["edge_cases"]["edge_cases"] = edge_cases_with_strategies

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
                    self.console.print(f"- [bold]{edge_case['edge_case']}[/bold]")
                    if edge_case["prevention"]:
                        self.console.print("    [green]Prevention:[/green]")
                        self.display_helper.display_list(edge_case["prevention"], prefix="      -")
                    if edge_case["mitigation"]:
                        self.console.print("    [yellow]Mitigation:[/yellow]")
                        self.display_helper.display_list(edge_case["mitigation"], prefix="      -")
            
            if design_data["edge_cases"]["small_scale"]:
                self.console.print("\n[bold]Small Scale Failures:[/bold]")
                for failure in design_data["edge_cases"]["small_scale"]:
                    self.console.print(f"- [bold]{failure['failure']}[/bold]")
                    if failure.get("prevention"):
                        self.console.print("    [green]Prevention:[/green]")
                        self.display_helper.display_list(failure["prevention"], prefix="      -")
                    if failure.get("mitigation"):
                        self.console.print("    [yellow]Mitigation:[/yellow]")
                        self.display_helper.display_list(failure["mitigation"], prefix="      -")
            
            if design_data["edge_cases"]["large_scale"]:
                self.console.print("\n[bold]Large Scale Failures:[/bold]")
                for failure in design_data["edge_cases"]["large_scale"]:
                    self.console.print(f"- [bold]{failure['failure']}[/bold]")
                    if failure.get("prevention"):
                        self.console.print("    [green]Prevention:[/green]")
                        self.display_helper.display_list(failure["prevention"], prefix="      -")
                    if failure.get("mitigation"):
                        self.console.print("    [yellow]Mitigation:[/yellow]")
                        self.display_helper.display_list(failure["mitigation"], prefix="      -")
        
        return design_data 