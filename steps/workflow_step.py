from .base_step import BaseStep

class WorkflowStep(BaseStep):
    def execute(self, design_data):
        """Design workflows for each API."""
        self.console.print("\n[bold]Step 3: Workflow Design[/bold]")
        
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
                        api_choices.append((f"Internal: {api['endpoint']} {req_summary}->{resp_summary}", api, req))
            if design_data["apis"]["external"]:
                for api in design_data["apis"]["external"]:
                    if api["endpoint"] not in seen_apis:
                        seen_apis.add(api["endpoint"])
                        # Format request/response summary
                        req_summary = "{}" if not api["request"] else " ".join(api["request"])
                        resp_summary = "{}" if not api["response"] else " ".join(api["response"])
                        api_choices.append((f"External: {api['endpoint']} {req_summary}->{resp_summary}", api, req))

        if not api_choices:
            self.console.print("[yellow]No APIs defined yet. Please define APIs first.[/yellow]")
            return design_data

        self.console.print("\n[bold]Select an API to design its workflow:[/bold]")
        for i, (api_desc, _, _) in enumerate(api_choices, 1):
            self.console.print(f"{i}. {api_desc}")

        # Initialize workflows list if it doesn't exist
        if "workflows" not in design_data:
            design_data["workflows"] = []

        while True:
            # Only show 'done' option if at least one workflow is defined
            choices = [str(i) for i in range(1, len(api_choices) + 1)]
            if design_data["workflows"]:
                choices.append("done")
            
            choice = self.prompt.ask(
                "Select an API to design its workflow" + (" (or 'done' to finish)" if design_data["workflows"] else ""),
                choices=choices
            )
            
            if choice == "done":
                break
                
            selected_api = api_choices[int(choice) - 1]
            api_desc, api, req = selected_api
            
            self.console.print(f"\n[bold]Designing workflow for: {api_desc}[/bold]")
            self.console.print(f"Requirement: {req}")
            
            # Get high-level workflow steps
            workflow_steps = self._get_multi_line_input(
                "Enter high-level workflow steps (one per line, x to finish):",
                "x"
            )
            
            # For each step, get detailed definition with substeps
            step_definitions = []
            for i, step in enumerate(workflow_steps, 1):
                self.console.print(f"\n[bold]Step {i}: {step}[/bold]")
                substeps = self._get_multi_line_input(
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
                "steps": step_definitions
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
        
        return design_data 