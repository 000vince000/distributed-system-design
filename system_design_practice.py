import time
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from typing import List, Dict
import json
import os
from datetime import datetime

class SystemDesignPractice:
    def __init__(self):
        self.console = Console()
        self.start_time = None
        self.design_questions = self._load_questions()
        self.current_design = {
            "question": "",
            "requirements": {"functional": [], "nonfunctional": []},
            "apis": {"internal": [], "external": []},
            "workflows": [],
            "components": [],
            "optimizations": [],
            "edge_cases": {"small": [], "big": []}
        }

    def _get_multi_line_input(self, prompt: str, terminator: str = "") -> List[str]:
        """Get multi-line input from user until terminator is entered."""
        self.console.print(f"\n{prompt}")
        self.console.print(f"Enter {terminator} on a new line to finish.")
        lines = []
        while True:
            line = input()
            if line.strip() == terminator:
                break
            if line.strip():  # Only add non-empty lines
                lines.append(line.strip())
        return lines

    def _load_questions(self) -> Dict[str, str]:
        """Load questions from the question-bank directory."""
        questions = {}
        question_bank_dir = "question-bank"
        
        if not os.path.exists(question_bank_dir):
            self.console.print("[yellow]Warning: question-bank directory not found. Using default questions.[/yellow]")
            return {
                "1": "Design Facebook Newsfeed",
                "2": "Design Airbnb",
                "3": "Design Twitter",
                "4": "Design Uber",
                "5": "Design WhatsApp"
            }
        
        try:
            for filename in os.listdir(question_bank_dir):
                if filename.startswith('.'):
                    continue
                filepath = os.path.join(question_bank_dir, filename)
                if os.path.isfile(filepath):
                    with open(filepath, 'r') as f:
                        content = f.read().strip()
                        # Use the first line as the question title
                        title = content.split('\n')[0]
                        questions[str(len(questions) + 1)] = title
        except Exception as e:
            self.console.print(f"[red]Error loading questions: {str(e)}[/red]")
            return {
                "1": "Design Facebook Newsfeed",
                "2": "Design Airbnb",
                "3": "Design Twitter",
                "4": "Design Uber",
                "5": "Design WhatsApp"
            }
        
        return questions

    def _get_question_details(self, question_key: str) -> str:
        """Get the full details of a selected question."""
        question_bank_dir = "question-bank"
        try:
            # Find the file that contains this question
            for filename in os.listdir(question_bank_dir):
                if filename.startswith('.'):
                    continue
                filepath = os.path.join(question_bank_dir, filename)
                if os.path.isfile(filepath):
                    with open(filepath, 'r') as f:
                        content = f.read().strip()
                        if content.split('\n')[0] == self.design_questions[question_key]:
                            return content
        except Exception as e:
            self.console.print(f"[yellow]Warning: Could not load question details: {str(e)}[/yellow]")
        
        return self.design_questions[question_key]

    def start(self):
        """Start the system design practice session."""
        try:
            self.start_time = time.time()
            self.console.print(Panel.fit("System Design Practice Tool", style="bold blue"))
            self.select_design_question()
        except Exception as e:
            self.console.print(f"[red]Error starting session: {str(e)}[/red]")
            raise

    def select_design_question(self):
        """Select a design question to work on."""
        self.console.print("\nAvailable Design Questions:")
        for key, value in self.design_questions.items():
            self.console.print(f"{key}. {value}")
        
        choice = Prompt.ask("Select a design question", choices=list(self.design_questions.keys()))
        self.current_design["question"] = self._get_question_details(choice)
        self.console.print("\n[bold]Selected Question:[/bold]")
        self.console.print(self.current_design["question"])
        self.gather_requirements()

    def gather_requirements(self):
        """Gather functional and non-functional requirements."""
        self.console.print("\n[bold]Step 1: Requirement Gathering[/bold]")
        
        self.console.print("\n[bold]Functional Requirements:[/bold]")
        self.current_design["requirements"]["functional"] = self._get_multi_line_input(
            "Enter functional requirements (one per line):",
            "END"
        )

        self.console.print("\n[bold]Non-functional Requirements:[/bold]")
        self.current_design["requirements"]["nonfunctional"] = self._get_multi_line_input(
            "Enter non-functional requirements (one per line):",
            "END"
        )

        self.design_apis()

    def design_apis(self):
        """Design internal and external APIs."""
        self.console.print("\n[bold]Step 2: API Design[/bold]")
        
        # Create a copy of functional requirements to track which ones have been addressed
        remaining_reqs = self.current_design["requirements"]["functional"].copy()
        self.current_design["apis"]["internal"] = []
        self.current_design["apis"]["external"] = []
        # Track which APIs belong to which requirement
        requirement_apis = {req: {"internal": None, "external": None} for req in self.current_design["requirements"]["functional"]}

        while remaining_reqs:
            self.console.print("\n[bold]Select a functional requirement to design APIs for:[/bold]")
            for i, req in enumerate(remaining_reqs, 1):
                self.console.print(f"{i}. {req}")
            
            self.console.print(f"{len(remaining_reqs) + 1}. Done with all requirements")
            
            choice = Prompt.ask(
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
            
            api_type = Prompt.ask(
                "Select API type",
                choices=["1", "2"]
            )
            
            api_type_name = "internal" if api_type == "1" else "external"
            self.console.print(f"\n[bold]Enter {api_type_name} API for '{selected_req}'[/bold]")
            api = self._get_multi_line_input(
                f"Enter {api_type_name} API endpoint:",
                "END"
            )[0]  # Take only the first line as the endpoint
            
            # Get request definition
            self.console.print("\n[bold]Request Definition:[/bold]")
            request_def = self._get_multi_line_input(
                "Enter request definition (one per line):",
                "END"
            )
            
            # Get response definition
            self.console.print("\n[bold]Response Definition:[/bold]")
            response_def = self._get_multi_line_input(
                "Enter response definition (one per line):",
                "END"
            )
            
            # Store the complete API definition
            api_definition = {
                "endpoint": api,
                "request": request_def,
                "response": response_def
            }
            
            if api_type == "1":
                self.current_design["apis"]["internal"].append(api_definition)
                requirement_apis[selected_req]["internal"] = api_definition
            else:
                self.current_design["apis"]["external"].append(api_definition)
                requirement_apis[selected_req]["external"] = api_definition
            
            # Remove the addressed requirement
            remaining_reqs.pop(int(choice) - 1)
            
            if remaining_reqs:
                self.console.print("\n[bold]Remaining requirements:[/bold]")
                for req in remaining_reqs:
                    self.console.print(f"- {req}")

        self.design_workflows()

    def design_workflows(self):
        """Design workflows for each API."""
        self.console.print("\n[bold]Step 3: Workflow Design[/bold]")
        
        # Create a list of all APIs with their requirements
        api_choices = []
        for req in self.current_design["requirements"]["functional"]:
            if self.current_design["apis"]["internal"]:
                for api in self.current_design["apis"]["internal"]:
                    api_choices.append((f"Internal: {api['endpoint']}", api, req))
            if self.current_design["apis"]["external"]:
                for api in self.current_design["apis"]["external"]:
                    api_choices.append((f"External: {api['endpoint']}", api, req))

        if not api_choices:
            self.console.print("[yellow]No APIs defined yet. Please define APIs first.[/yellow]")
            return

        self.console.print("\n[bold]Select an API to design its workflow:[/bold]")
        for i, (api_desc, _, req) in enumerate(api_choices, 1):
            self.console.print(f"{i}. {api_desc} (Requirement: {req})")

        while True:
            choice = Prompt.ask(
                "Select an API to design its workflow (or 'done' to finish)",
                choices=[str(i) for i in range(1, len(api_choices) + 1)] + ["done"]
            )
            
            if choice == "done":
                break
                
            selected_api = api_choices[int(choice) - 1]
            api_desc, api, req = selected_api
            
            self.console.print(f"\n[bold]Designing workflow for: {api_desc}[/bold]")
            self.console.print(f"Requirement: {req}")
            self.console.print(f"Request: {' '.join(api['request'])}")
            self.console.print(f"Response: {' '.join(api['response'])}")
            
            # Get high-level workflow steps
            workflow_steps = self._get_multi_line_input(
                "Enter high-level workflow steps (one per line):",
                "END"
            )
            
            # For each step, get detailed definition with substeps
            step_definitions = []
            for i, step in enumerate(workflow_steps, 1):
                self.console.print(f"\n[bold]Step {i}: {step}[/bold]")
                substeps = self._get_multi_line_input(
                    "Enter substeps (one per line, leave empty to skip):",
                    "END"
                )
                step_definitions.append({
                    "step": step,
                    "substeps": substeps
                })
            
            # Store the workflow
            if "workflows" not in self.current_design:
                self.current_design["workflows"] = []
            
            workflow = {
                "api": api["endpoint"],
                "requirement": req,
                "steps": step_definitions
            }
            
            self.current_design["workflows"].append(workflow)
            
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

        self.design_data_models()

    def design_data_models(self):
        """Design data models."""
        self.console.print("\n[bold]Step 4: Data Model Design[/bold]")
        self.current_design["components"] = self._get_multi_line_input(
            "Enter components (one per line):",
            "END"
        )

        self.optimize_design()

    def optimize_design(self):
        """Add design optimizations."""
        self.console.print("\n[bold]Step 5: Design Optimization[/bold]")
        self.current_design["optimizations"] = self._get_multi_line_input(
            "Enter optimizations (one per line):",
            "END"
        )

        self.identify_edge_cases()

    def identify_edge_cases(self):
        """Identify edge cases."""
        self.console.print("\n[bold]Step 6: Edge Cases[/bold]")
        
        self.console.print("\n[bold]Small Edge Cases:[/bold]")
        self.current_design["edge_cases"]["small"] = self._get_multi_line_input(
            "Enter small edge cases (one per line):",
            "END"
        )

        self.console.print("\n[bold]Big Edge Cases:[/bold]")
        self.current_design["edge_cases"]["big"] = self._get_multi_line_input(
            "Enter big edge cases (one per line):",
            "END"
        )

        self.generate_report()

    def generate_mermaid_diagram(self):
        """Generate a mermaid diagram from components and workflows."""
        try:
            diagram = ["graph TD"]
            
            # Add components as nodes
            for i, component in enumerate(self.current_design["components"]):
                safe_name = component.replace(" ", "_")
                diagram.append(f"    {safe_name}[{component}]")
            
            # Add workflows as connections
            for workflow in self.current_design["workflows"]:
                if "->" in workflow:
                    source, target = workflow.split("->", 1)
                    source = source.strip().replace(" ", "_")
                    if ":" in target:
                        target, action = target.split(":", 1)
                        target = target.strip().replace(" ", "_")
                        action = action.strip()
                        diagram.append(f"    {source} -->|{action}| {target}")
                    else:
                        target = target.strip().replace(" ", "_")
                        diagram.append(f"    {source} --> {target}")
            
            return "\n".join(diagram)
        except Exception as e:
            self.console.print(f"[yellow]Warning: Could not generate diagram: {str(e)}[/yellow]")
            return "graph TD\n    A[Error generating diagram]"

    def generate_report(self):
        """Generate the final report."""
        try:
            elapsed_time = time.time() - self.start_time
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"design_report_{timestamp}.md"

            # Generate mermaid diagram
            mermaid_diagram = self.generate_mermaid_diagram()

            report = f"""# System Design Practice Report

## Design Question
{self.current_design['question']}

## Time Taken
{elapsed_time:.2f} seconds

## Requirements
### Functional
{chr(10).join(f"- {req}" for req in self.current_design['requirements']['functional'])}

### Non-functional
{chr(10).join(f"- {req}" for req in self.current_design['requirements']['nonfunctional'])}

## APIs
### Internal
{chr(10).join(f"- {api}" for api in self.current_design['apis']['internal'])}

### External
{chr(10).join(f"- {api}" for api in self.current_design['apis']['external'])}

## Workflows
{chr(10).join(f"- {workflow}" for workflow in self.current_design['workflows'])}

## Components
{chr(10).join(f"- {component}" for component in self.current_design['components'])}

## System Architecture
```mermaid
{mermaid_diagram}
```

## Optimizations
{chr(10).join(f"- {opt}" for opt in self.current_design['optimizations'])}

## Edge Cases
### Small
{chr(10).join(f"- {case}" for case in self.current_design['edge_cases']['small'])}

### Big
{chr(10).join(f"- {case}" for case in self.current_design['edge_cases']['big'])}
"""

            with open(filename, 'w') as f:
                f.write(report)

            self.console.print(f"\n[green]Report generated successfully![/green]")
            self.console.print(f"File saved as: {filename}")
            self.console.print("\n[bold]Report Preview:[/bold]")
            self.console.print(Markdown(report))
        except Exception as e:
            self.console.print(f"[red]Error generating report: {str(e)}[/red]")

if __name__ == "__main__":
    practice = SystemDesignPractice()
    practice.start() 