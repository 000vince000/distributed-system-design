from .base_step import BaseStep
from .helpers import InputHelper, DisplayHelper, StepNavigationHelper

class ApiStep(BaseStep):
    def execute(self, design_data):
        """Design external APIs for each functional requirement.

        Internal/downstream APIs aren't designed here — they get captured
        later, inline during workflow design (step 3), once a candidate
        actually discovers a step needs one.
        """
        self.navigation_helper.display_step_header(2)

        # Create a copy of functional requirements to track which ones have been addressed
        remaining_reqs = design_data["requirements"]["functional"].copy()
        design_data["apis"]["internal"] = []
        design_data["apis"]["external"] = []

        while remaining_reqs:
            self.console.print("\n[bold]Select a functional requirement to design an API for:[/bold]")
            self.display_helper.display_list(remaining_reqs, enumerate_items=True)

            self.console.print("x. Done with all requirements")

            choices = [str(i) for i in range(1, len(remaining_reqs) + 1)] + [self.input_helper.SKIP_CHOICE]
            choice = self.input_helper.get_choice(
                "Select a requirement to design an API for",
                choices=choices,
                show_choices=False
            )

            if choice == self.input_helper.SKIP_CHOICE:
                break

            selected_req = remaining_reqs[int(choice) - 1]

            self.console.print(f"\n[bold]Designing external API for: {selected_req}[/bold]")
            api = self.input_helper.get_multi_line_input(
                f"Enter external API endpoint for '{selected_req}'"
            )[0]

            # Get request definition
            request_def = self.input_helper.get_multi_line_input(
                "Enter request definition (one per line, empty line to finish):"
            )

            # Get response definition
            response_def = self.input_helper.get_multi_line_input(
                "Enter response definition (one per line, empty line to finish):"
            )

            # Store the complete API definition with the selected requirement
            api_definition = {
                "endpoint": api,
                "request": request_def,
                "response": response_def,
                "requirement": selected_req  # Use the requirement selected in step 1
            }

            design_data["apis"]["external"].append(api_definition)

            # Remove the addressed requirement
            remaining_reqs.pop(int(choice) - 1)

        return design_data 