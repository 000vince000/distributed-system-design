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
            
            self.console.print(f"{len(remaining_reqs) + 1}. Done with all requirements")
            
            choice = self.prompt.ask(
                "Select a requirement to design APIs for",
                choices=[str(i) for i in range(1, len(remaining_reqs) + 2)]
            )
            
            if int(choice) == len(remaining_reqs) + 1:
                break
                
            selected_req = remaining_reqs[int(choice) - 1]
            
            # Get API type
            self.console.print(f"\n[bold]Designing APIs for: {selected_req}[/bold]")
            self.console.print("1. Internal API")
            self.console.print("2. External API")
            
            api_type = self.prompt.ask(
                "Select API type",
                choices=["1", "2"]
            )
            
            api_type_name = "internal" if api_type == "1" else "external"
            api = self._get_multi_line_input(
                f"Enter {api_type_name} API endpoint for '{selected_req}'",
                "END"
            )[0]  # Take only the first line as the endpoint
            
            # Get request definition
            request_def = self._get_multi_line_input(
                "Enter request definition (one per line, END to finish):",
                "END"
            )
            
            # Get response definition
            response_def = self._get_multi_line_input(
                "Enter response definition (one per line, END to finish):",
                "END"
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