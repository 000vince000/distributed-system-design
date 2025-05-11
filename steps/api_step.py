from .base_step import BaseStep

class ApiStep(BaseStep):
    def execute(self, design_data):
        """Design internal and external APIs."""
        self.console.print("\n[bold]Step 2: API Design[/bold]")
        
        # Create a copy of functional requirements to track which ones have been addressed
        remaining_reqs = design_data["requirements"]["functional"].copy()
        design_data["apis"]["internal"] = []
        design_data["apis"]["external"] = []
        # Track which APIs belong to which requirement
        requirement_apis = {req: {"internal": None, "external": None} for req in design_data["requirements"]["functional"]}

        while remaining_reqs:
            self.console.print("\n[bold]Select a functional requirement to design APIs for:[/bold]")
            for i, req in enumerate(remaining_reqs, 1):
                self.console.print(f"{i}. {req}")
            
            self.console.print("x. Done with all requirements")
            
            choices = [str(i) for i in range(1, len(remaining_reqs) + 1)] + ["x"]
            prompt_kwargs = {
                "prompt": "Select a requirement to design APIs for",
                "choices": choices
            }
            if len(choices) == 2:  # Only one requirement + 'x'
                prompt_kwargs["default"] = choices[0]
            choice = self.prompt.ask(**prompt_kwargs)
            
            if choice == "x":
                break
            
            selected_req = remaining_reqs[int(choice) - 1]
            
            # Get API type
            self.console.print(f"\n[bold]Designing APIs for: {selected_req}[/bold]")
            self.console.print("1. External API")
            self.console.print("2. Internal API")
            
            api_type = self.prompt.ask(
                "Select API type",
                choices=["1", "2"]
            )
            
            api_type_name = "external" if api_type == "1" else "internal"
            api = self._get_multi_line_input(
                f"Enter {api_type_name} API endpoint for '{selected_req}'",
                "x"
            )[0]
            
            # Get request definition
            request_def = self._get_multi_line_input(
                "Enter request definition (one per line, x to finish):",
                "x"
            )
            
            # Get response definition
            response_def = self._get_multi_line_input(
                "Enter response definition (one per line, x to finish):",
                "x"
            )
            
            # Store the complete API definition
            api_definition = {
                "endpoint": api,
                "request": request_def,
                "response": response_def
            }
            
            if api_type == "1":
                design_data["apis"]["internal"].append(api_definition)
                requirement_apis[selected_req]["internal"] = api_definition
            else:
                design_data["apis"]["external"].append(api_definition)
                requirement_apis[selected_req]["external"] = api_definition
            
            # Remove the addressed requirement
            remaining_reqs.pop(int(choice) - 1)
            
            if remaining_reqs:
                self.console.print("\n[bold]Remaining requirements:[/bold]")
                for req in remaining_reqs:
                    self.console.print(f"- {req}")
        
        return design_data 