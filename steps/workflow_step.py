from .base_step import BaseStep
from .helpers import InputHelper, DisplayHelper, StepNavigationHelper

class WorkflowStep(BaseStep):
    def __init__(self, console=None):
        super().__init__(console)
        self.input_helper = InputHelper(self.console, self.prompt)
        self.display_helper = DisplayHelper(self.console)
        self.nav_helper = StepNavigationHelper(self.console, self.prompt)

    def execute(self, design_data):
        """Design workflows for each API."""
        self.nav_helper.display_step_header(3)
        
        # Create a list of all APIs with their requirements
        api_choices = []
        seen_apis = set()  # Track unique APIs
        
        # Collect APIs from both internal and external
        for req in design_data["requirements"]["functional"]:
            if design_data["apis"]["internal"]:
                for api in design_data["apis"]["internal"]:
                    if api["endpoint"] not in seen_apis:
                        seen_apis.add(api["endpoint"])
                        # Format request/response summary
                        req_summary = "{}" if not api["request"] else " ".join(api["request"])
                        resp_summary = "{}" if not api["response"] else " ".join(api["response"])
                        api_choices.append((f"Internal: {api['endpoint']} {req_summary}->{resp_summary}", api, req, "internal"))
            if design_data["apis"]["external"]:
                for api in design_data["apis"]["external"]:
                    if api["endpoint"] not in seen_apis:
                        seen_apis.add(api["endpoint"])
                        # Format request/response summary
                        req_summary = "{}" if not api["request"] else " ".join(api["request"])
                        resp_summary = "{}" if not api["response"] else " ".join(api["response"])
                        api_choices.append((f"External: {api['endpoint']} {req_summary}->{resp_summary}", api, req, "external"))

        if not api_choices:
            self.console.print("[yellow]No APIs defined yet. Please define APIs first.[/yellow]")
            return design_data

        # Initialize workflows list if it doesn't exist
        if "workflows" not in design_data:
            design_data["workflows"] = []

        # Show existing workflows if any
        if design_data["workflows"]:
            self.console.print("\n[bold]Existing Workflows:[/bold]")
            for workflow in design_data["workflows"]:
                self.console.print(f"\nAPI: {workflow['api']}")
                self.console.print(f"Requirement: {workflow['requirement']}")
                self.console.print("Steps:")
                for step in workflow["steps"]:
                    self.console.print(f"  {step['step']}")
                    for substep in step["substeps"]:
                        self.console.print(f"    - {substep}")

        # Filter out APIs that already have workflows
        available_apis = []
        for api_desc, api, req, api_type in api_choices:
            # Check if this API already has a workflow
            if not any(w["api"] == api["endpoint"] for w in design_data["workflows"]):
                available_apis.append((api_desc, api, req, api_type))

        if not available_apis:
            self.console.print("\n[yellow]No more APIs available to design workflows for.[/yellow]")
            return design_data

        self.console.print("\n[bold]Select an API to design its workflow:[/bold]")
        for i, (api_desc, _, _, api_type) in enumerate(available_apis, 1):
            self.console.print(f"{i}. {api_desc} ({api_type})")

        while True:
            # Only show 'x' option if at least one workflow is defined
            choices = [str(i) for i in range(1, len(available_apis) + 1)]
            if design_data["workflows"]:
                choices.append("x")
            
            choice = self.input_helper.get_choice(
                "Select an API to design its workflow" + (" (or 'x' to finish)" if design_data["workflows"] else ""),
                choices=choices
            )
            
            if choice == "x":
                break
                
            selected_api = available_apis[int(choice) - 1]
            api_desc, api, req, api_type = selected_api
            
            self.console.print(f"\n[bold]Designing workflow for: {api_desc}[/bold]")
            self.console.print(f"Requirement: {req}")
            
            # Get high-level workflow steps
            workflow_steps = self.input_helper.get_multi_line_input(
                "Enter high-level workflow steps (one per line, x to finish):",
                "x"
            )
            
            # For each step, get detailed definition with substeps
            step_definitions = []
            for i, step in enumerate(workflow_steps, 1):
                self.console.print(f"\n[bold]Step {i}: {step}[/bold]")
                substeps = self.input_helper.get_multi_line_input(
                    "Enter substeps (one per line, x to finish):",
                    "x"
                )
                step_definitions.append({
                    "step": step,
                    "substeps": substeps
                })
            
            workflow = {
                "api": api["endpoint"],
                "requirement": req,
                "steps": step_definitions,
                "type": api_type  # Add API type to workflow
            }
            
            design_data["workflows"].append(workflow)
            
            # Display summary of the current workflow
            self.console.print("\n[bold]Workflow Summary:[/bold]")
            self.console.print(f"API: {workflow['api']}")
            self.console.print(f"Requirement: {workflow['requirement']}")
            self.console.print("\nSteps:")
            for step_def in workflow["steps"]:
                self.console.print(f"\n  {step_def['step']}")
                if step_def["substeps"]:
                    for substep in step_def["substeps"]:
                        self.console.print(f"    - {substep}")
            
            # Update available APIs list
            available_apis = []
            for api_desc, api, req, api_type in api_choices:
                # Check if this API already has a workflow
                if not any(w["api"] == api["endpoint"] for w in design_data["workflows"]):
                    available_apis.append((api_desc, api, req, api_type))
            
            if not available_apis:
                self.console.print("\n[yellow]No more APIs available to design workflows for.[/yellow]")
                break
                
            # Display available APIs again before next selection
            self.console.print("\n[bold]Available APIs:[/bold]")
            for i, (api_desc, _, _, api_type) in enumerate(available_apis, 1):
                self.console.print(f"{i}. {api_desc} ({api_type})")
        
        return design_data 