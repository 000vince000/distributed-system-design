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
        self.design_questions = {
            "1": "Design Facebook Newsfeed",
            "2": "Design Airbnb",
            "3": "Design Twitter",
            "4": "Design Uber",
            "5": "Design WhatsApp"
        }
        self.current_design = {
            "question": "",
            "requirements": {"functional": [], "nonfunctional": []},
            "apis": {"internal": [], "external": []},
            "workflows": [],
            "components": [],
            "optimizations": [],
            "edge_cases": {"small": [], "big": []}
        }

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
        
        choice = Prompt.ask("Select a design question (1-5)", choices=list(self.design_questions.keys()))
        self.current_design["question"] = self.design_questions[choice]
        self.gather_requirements()

    def gather_requirements(self):
        """Gather functional and non-functional requirements."""
        self.console.print("\n[bold]Step 1: Requirement Gathering[/bold]")
        
        self.console.print("\n[bold]Functional Requirements:[/bold]")
        while True:
            req = Prompt.ask("Add a functional requirement (or press Enter to finish)")
            if not req:
                break
            self.current_design["requirements"]["functional"].append(req)

        self.console.print("\n[bold]Non-functional Requirements:[/bold]")
        while True:
            req = Prompt.ask("Add a non-functional requirement (or press Enter to finish)")
            if not req:
                break
            self.current_design["requirements"]["nonfunctional"].append(req)

        self.design_apis()

    def design_apis(self):
        """Design internal and external APIs."""
        self.console.print("\n[bold]Step 2: API Design[/bold]")
        
        self.console.print("\n[bold]Internal APIs:[/bold]")
        while True:
            api = Prompt.ask("Add an internal API (or press Enter to finish)")
            if not api:
                break
            self.current_design["apis"]["internal"].append(api)

        self.console.print("\n[bold]External APIs:[/bold]")
        while True:
            api = Prompt.ask("Add an external API (or press Enter to finish)")
            if not api:
                break
            self.current_design["apis"]["external"].append(api)

        self.design_workflows()

    def design_workflows(self):
        """Design system workflows."""
        self.console.print("\n[bold]Step 3: Workflow Design[/bold]")
        self.console.print("Format: ComponentA -> ComponentB: action")
        while True:
            workflow = Prompt.ask("Add a workflow (or press Enter to finish)")
            if not workflow:
                break
            self.current_design["workflows"].append(workflow)

        self.identify_components()

    def identify_components(self):
        """Identify system components."""
        self.console.print("\n[bold]Step 4: Component Identification[/bold]")
        while True:
            component = Prompt.ask("Add a component (or press Enter to finish)")
            if not component:
                break
            self.current_design["components"].append(component)

        self.optimize_design()

    def optimize_design(self):
        """Add design optimizations."""
        self.console.print("\n[bold]Step 5: Design Optimization[/bold]")
        while True:
            optimization = Prompt.ask("Add an optimization (or press Enter to finish)")
            if not optimization:
                break
            self.current_design["optimizations"].append(optimization)

        self.identify_edge_cases()

    def identify_edge_cases(self):
        """Identify edge cases."""
        self.console.print("\n[bold]Step 6: Edge Cases[/bold]")
        
        self.console.print("\n[bold]Small Edge Cases:[/bold]")
        while True:
            case = Prompt.ask("Add a small edge case (or press Enter to finish)")
            if not case:
                break
            self.current_design["edge_cases"]["small"].append(case)

        self.console.print("\n[bold]Big Edge Cases:[/bold]")
        while True:
            case = Prompt.ask("Add a big edge case (or press Enter to finish)")
            if not case:
                break
            self.current_design["edge_cases"]["big"].append(case)

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