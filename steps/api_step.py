from .base_step import BaseStep
from .helpers import InputHelper, DisplayHelper, StepNavigationHelper

class ApiStep(BaseStep):
    def execute(self, design_data):
        """Design internal and external APIs."""
        self.navigation_helper.display_step_header(2)
        
        # Create a copy of functional requirements to track which ones have been addressed
        remaining_reqs = design_data["requirements"]["functional"].copy()
        design_data["apis"]["internal"] = []
        design_data["apis"]["external"] = []
        # Track which APIs belong to which requirement
        requirement_apis = {req: {"internal": None, "external": None} for req in design_data["requirements"]["functional"]}

        while remaining_reqs:
            self.console.print("\n[bold]Select a functional requirement to design APIs for:[/bold]")
            self.display_helper.display_list(remaining_reqs, enumerate_items=True)
            
            self.console.print("x. Done with all requirements")
            
            choices = [str(i) for i in range(1, len(remaining_reqs) + 1)] + [self.input_helper.SKIP_CHOICE]
            choice = self.input_helper.get_choice(
                "Select a requirement to design APIs for",
                choices=choices
            )
            
            if choice == self.input_helper.SKIP_CHOICE:
                break
            
            selected_req = remaining_reqs[int(choice) - 1]
            
            # Get API type
            self.console.print(f"\n[bold]Designing APIs for: {selected_req}[/bold]")
            api_options = ["External API", "Internal API"]
            self.display_helper.display_list(api_options, enumerate_items=True)
            
            api_type = self.input_helper.get_choice(
                "Select API type",
                choices=["1", "2"]
            )
            
            api_type_name = "external" if api_type == "1" else "internal"
            api = self.input_helper.get_multi_line_input(
                f"Enter {api_type_name} API endpoint for '{selected_req}'"
            )[0]
            
            # Get request definition
            request_def = self.input_helper.get_multi_line_input(
                "Enter request definition (one per line, x to finish):"
            )
            
            # Get response definition
            response_def = self.input_helper.get_multi_line_input(
                "Enter response definition (one per line, x to finish):"
            )
            
            # Store the complete API definition with the selected requirement
            api_definition = {
                "endpoint": api,
                "request": request_def,
                "response": response_def,
                "requirement": selected_req  # Use the requirement selected in step 1
            }
            
            if api_type == "1":  # External API
                design_data["apis"]["external"].append(api_definition)
            else:  # Internal API
                design_data["apis"]["internal"].append(api_definition)
            
            # Remove the addressed requirement
            remaining_reqs.pop(int(choice) - 1)
            
            if remaining_reqs:
                self.console.print("\n[bold]Remaining requirements:[/bold]")
                self.display_helper.display_list(remaining_reqs)
        
        return design_data 