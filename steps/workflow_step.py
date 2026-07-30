from rich.markup import escape
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
        self.nav_helper.display_step_header(4)
        
        # Create a list of all APIs with their requirements.
        # Internal/downstream APIs are intentionally excluded here — they're
        # only ever discovered and fully specified inline, as an attachment
        # to another workflow's step (see api_step.py), so by the time one
        # exists it's already complete and isn't itself a candidate for a
        # top-level workflow.
        api_choices = []
        seen_apis = set()  # Track unique APIs

        if design_data["apis"]["external"]:
            for api in design_data["apis"]["external"]:
                if api["endpoint"] not in seen_apis:
                    seen_apis.add(api["endpoint"])
                    # Format request/response summary
                    req_summary = "{}" if not api["request"] else " ".join(api["request"])
                    resp_summary = "{}" if not api["response"] else " ".join(api["response"])
                    api_choices.append((f"External: {api['endpoint']} {req_summary}->{resp_summary}", api, api["requirement"], "external"))

        if not api_choices:
            self.console.print("[warning]No APIs defined yet. Please define APIs first.[/warning]")
            return design_data

        # Initialize workflows list if it doesn't exist
        if "workflows" not in design_data:
            design_data["workflows"] = []

        # Show existing workflows if any
        if design_data["workflows"]:
            self.console.print("\n[bold]Existing Workflows:[/bold]")
            for workflow in design_data["workflows"]:
                self.console.print(f"\nAPI: {escape(workflow['api'])}")
                self.console.print(f"Requirement: {escape(workflow['requirement'])}")
                self.console.print("Steps:")
                for step in workflow["steps"]:
                    self.console.print(f"  {escape(step['step'])}")
                    for substep in step["substeps"]:
                        self.console.print(f"    - {escape(substep)}")

        # Filter out APIs that already have workflows
        available_apis = []
        for api_desc, api, req, api_type in api_choices:
            # Check if this API already has a workflow
            if not any(w["api"] == api["endpoint"] for w in design_data["workflows"]):
                available_apis.append((api_desc, api, req, api_type))

        if not available_apis:
            self.console.print("\n[warning]No more APIs available to design workflows for.[/warning]")
            return design_data

        self.console.print("\n[bold]Select an API to design its workflow:[/bold]")
        for i, (api_desc, _, _, api_type) in enumerate(available_apis, 1):
            self.console.print(f"{i}. {escape(api_desc)} ({api_type})")

        while True:
            # Only show 'x' option if at least one workflow is defined
            choices = [str(i) for i in range(1, len(available_apis) + 1)]
            if design_data["workflows"]:
                choices.append(self.input_helper.SKIP_CHOICE)
            
            choice = self.input_helper.get_choice(
                "Select an API to design its workflow" + (" (or 'x' to finish)" if design_data["workflows"] else ""),
                choices=choices,
                show_choices=False
            )
            
            if choice == self.input_helper.SKIP_CHOICE:
                break
                
            selected_api = available_apis[int(choice) - 1]
            api_desc, api, req, api_type = selected_api
            
            self.console.print(f"\n[bold]Designing workflow for: {escape(api_desc)}[/bold]")
            self.console.print(f"Requirement: {escape(req)}")
            
            # Get high-level workflow steps
            workflow_steps = self.input_helper.get_multi_line_input(
                "Enter high-level workflow steps (one per line, empty line to finish):"
            )

            # Commit the workflow to design_data immediately, and fill in its
            # steps in place as they're completed, so a mid-workflow quit
            # doesn't lose steps already finished.
            workflow = {
                "api": api["endpoint"],
                "requirement": req,
                "steps": [],
                "type": api_type
            }
            design_data["workflows"].append(workflow)

            for i, step in enumerate(workflow_steps, 1):
                self.console.print(f"\n[bold]Step {i}: {escape(step)}[/bold]")

                # Most steps have neither substeps nor a new internal/downstream
                # API call, so gate both behind a single skippable question
                # instead of always forcing the substeps prompt.
                substeps = []
                step_internal_apis = []
                if self.input_helper.get_choice(
                    f"Does '{step}' have substeps or need an internal/downstream API call?",
                    choices=["y", "n"]
                ) == "y":
                    substeps = self.input_helper.get_multi_line_input(
                        "Enter substeps, if any (one per line, empty line to finish):"
                    )

                    if self.input_helper.get_choice(
                        f"Does '{step}' require a new internal/downstream API call?",
                        choices=["y", "n"]
                    ) == "y":
                        internal_endpoint = self.input_helper.get_multi_line_input(
                            "Enter internal API endpoint:"
                        )
                        if internal_endpoint:
                            internal_request = self.input_helper.get_multi_line_input(
                                "Enter request definition (one per line, empty line to finish):"
                            )
                            internal_response = self.input_helper.get_multi_line_input(
                                "Enter response definition (one per line, empty line to finish):"
                            )

                            internal_api = {
                                "endpoint": internal_endpoint[0],
                                "request": internal_request,
                                "response": internal_response,
                                "requirement": req,
                                "workflow_api": api["endpoint"]
                            }
                            design_data["apis"]["internal"].append(internal_api)
                            step_internal_apis.append(internal_api["endpoint"])

                workflow["steps"].append({
                    "step": step,
                    "substeps": substeps,
                    "internal_apis": step_internal_apis
                })

            # Display summary of the current workflow
            self.console.print("\n[bold]Workflow Summary:[/bold]")
            self.console.print(f"API: {escape(workflow['api'])}")
            self.console.print(f"Requirement: {escape(workflow['requirement'])}")
            self.console.print("\nSteps:")
            for step_def in workflow["steps"]:
                self.console.print(f"\n  {escape(step_def['step'])}")
                if step_def["substeps"]:
                    for substep in step_def["substeps"]:
                        self.console.print(f"    - {escape(substep)}")
            
            # Update available APIs list
            available_apis = []
            for api_desc, api, req, api_type in api_choices:
                # Check if this API already has a workflow
                if not any(w["api"] == api["endpoint"] for w in design_data["workflows"]):
                    available_apis.append((api_desc, api, req, api_type))
            
            if not available_apis:
                self.console.print("\n[warning]No more APIs available to design workflows for.[/warning]")
                break
                
            # Display available APIs again before next selection
            self.console.print("\n[bold]Available APIs:[/bold]")
            for i, (api_desc, _, _, api_type) in enumerate(available_apis, 1):
                self.console.print(f"{i}. {escape(api_desc)} ({api_type})")
        
        return design_data 