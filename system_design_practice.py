import time
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from typing import List, Dict
import json
import os
from datetime import datetime

from steps.requirements_step import RequirementsStep
from steps.api_step import ApiStep
from steps.workflow_step import WorkflowStep
from steps.architecture_step import ArchitectureStep
from steps.optimization_step import OptimizationStep
from steps.edge_cases_step import EdgeCasesStep

class SystemDesignPractice:
    def __init__(self):
        self.console = Console()
        self.prompt = Prompt()
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
        
        # Initialize steps
        self.steps = [
            RequirementsStep(self.console),
            ApiStep(self.console),
            WorkflowStep(self.console),
            ArchitectureStep(self.console),
            OptimizationStep(self.console),
            EdgeCasesStep(self.console)
        ]

    def _get_multi_line_input(self, prompt: str, terminator: str = "") -> List[str]:
        """Get multi-line input from user until terminator is entered."""
        self.console.print(f"\n{prompt}")
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
        
        # Execute each step in sequence
        for step in self.steps:
            self.current_design = step.execute(self.current_design)
        
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