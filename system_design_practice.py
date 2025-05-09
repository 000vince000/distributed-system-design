import time
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from typing import List, Dict
import json
import os
from datetime import datetime
import argparse

from steps.requirements_step import RequirementsStep
from steps.api_step import ApiStep
from steps.workflow_step import WorkflowStep
from steps.architecture_step import ArchitectureStep
from steps.optimization_step import OptimizationStep
from steps.edge_cases_step import EdgeCasesStep
from stubs.design_stubs import get_step1_stub, get_step2_stub, get_step3_stub, get_step4_stub, get_step5_stub, get_step6_stub

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

    def _display_stub_summary(self, step_number: int):
        """Display a summary of the stub data for a given step."""
        step_names = {
            1: "Requirements",
            2: "APIs",
            3: "Workflows",
            4: "Architecture",
            5: "Optimizations",
            6: "Edge Cases"
        }
        
        self.console.print(f"\n[bold blue]Step {step_number}: {step_names[step_number]} Summary[/bold blue]")
        
        if step_number == 1:
            self.console.print("\n[bold]Functional Requirements:[/bold]")
            for req in self.current_design["requirements"]["functional"]:
                self.console.print(f"- {req}")
            self.console.print("\n[bold]Non-functional Requirements:[/bold]")
            for req in self.current_design["requirements"]["nonfunctional"]:
                self.console.print(f"- {req}")
        
        elif step_number == 2:
            self.console.print("\n[bold]Internal APIs:[/bold]")
            for api in self.current_design["apis"]["internal"]:
                self.console.print(f"- {api['endpoint']}")
                self.console.print(f"  Request: {', '.join(api['request'])}")
                self.console.print(f"  Response: {', '.join(api['response'])}")
            self.console.print("\n[bold]External APIs:[/bold]")
            for api in self.current_design["apis"]["external"]:
                self.console.print(f"- {api['endpoint']}")
                self.console.print(f"  Request: {', '.join(api['request'])}")
                self.console.print(f"  Response: {', '.join(api['response'])}")
        
        elif step_number == 3:
            self.console.print("\n[bold]Workflows:[/bold]")
            for workflow in self.current_design["workflows"]:
                self.console.print(f"\nAPI: {workflow['api']}")
                self.console.print(f"Requirement: {workflow['requirement']}")
                self.console.print("Steps:")
                for step in workflow["steps"]:
                    self.console.print(f"  {step['step']}")
                    for substep in step["substeps"]:
                        self.console.print(f"    - {substep}")
        
        elif step_number == 4:
            if "architecture" in self.current_design:
                self.console.print("\n[bold]Component Types:[/bold]")
                for comp, type_ in self.current_design["architecture"]["component_types"].items():
                    self.console.print(f"- {comp}: {type_}")
                
                self.console.print("\n[bold]Relationships:[/bold]")
                for rel in self.current_design["architecture"]["relationships"]:
                    self.console.print(f"- {rel['relationship']}")
                    self.console.print(f"  Description: {rel['description']}")
                    self.console.print(f"  Protocol: {rel['protocol']}")
                
                if "database_schema" in self.current_design["architecture"]:
                    self.console.print("\n[bold]Database Schema:[/bold]")
                    for schema in self.current_design["architecture"]["database_schema"]:
                        self.console.print(f"- {schema}")
                
                # Generate and display Mermaid diagram
                architecture_step = ArchitectureStep(self.console)
                mermaid_diagram = architecture_step._generate_mermaid_diagram(self.current_design)
                self.console.print("\n[bold]Architecture Diagram:[/bold]")
                self.console.print("```mermaid")
                self.console.print(mermaid_diagram)
                self.console.print("```")
        
        elif step_number == 5:
            if "optimizations" in self.current_design:
                self.console.print("\n[bold]Optimizations:[/bold]")
                for opt in self.current_design["optimizations"]:
                    self.console.print(f"- {opt}")
        
        elif step_number == 6:
            if "edge_cases" in self.current_design:
                self.console.print("\n[bold]Small Edge Cases:[/bold]")
                for case in self.current_design["edge_cases"]["small"]:
                    self.console.print(f"- {case}")
                self.console.print("\n[bold]Big Edge Cases:[/bold]")
                for case in self.current_design["edge_cases"]["big"]:
                    self.console.print(f"- {case}")

    def start(self, start_step: int = 1):
        """Start the system design practice session."""
        try:
            self.start_time = time.time()
            self.console.print(Panel.fit("System Design Practice Tool", style="bold blue"))
            
            # If starting from a specific step, load stub data
            if start_step > 1:
                stub_functions = {
                    2: get_step1_stub,
                    3: get_step2_stub,
                    4: get_step3_stub,
                    5: get_step4_stub,
                    6: get_step5_stub
                }
                if start_step in stub_functions:
                    self.current_design = stub_functions[start_step]()
                    self.console.print(f"\n[bold]Starting from Step {start_step} with stub data[/bold]")
                    
                    # Display summaries of all previous steps
                    self.console.print("\n[bold yellow]Previous Steps Summary:[/bold yellow]")
                    for step in range(1, start_step):
                        self._display_stub_summary(step)
                else:
                    self.console.print("[red]Invalid start step number[/red]")
                    return
            
            self.select_design_question(start_step)
        except Exception as e:
            self.console.print(f"[red]Error starting session: {str(e)}[/red]")
            raise

    def select_design_question(self, start_step: int = 1):
        """Select a design question to work on."""
        if not self.current_design["question"]:
            self.console.print("\nAvailable Design Questions:")
            for key, value in self.design_questions.items():
                self.console.print(f"{key}. {value}")
            
            choice = Prompt.ask("Select a design question", choices=list(self.design_questions.keys()))
            self.current_design["question"] = self._get_question_details(choice)
            self.console.print("\n[bold]Selected Question:[/bold]")
            self.console.print(self.current_design["question"])
        
        # Execute steps starting from the specified step
        for i, step in enumerate(self.steps[start_step-1:], start=start_step):
            self.current_design = step.execute(self.current_design)
        
        self.generate_report()

    def generate_mermaid_diagram(self):
        """Generate a mermaid diagram from components and workflows."""
        try:
            if "architecture" not in self.current_design:
                return "graph TD\n    A[No architecture defined]"

            diagram = ["graph TD"]
            
            # Add components with their types
            for comp, type_ in self.current_design["architecture"]["component_types"].items():
                if type_ == "API":
                    diagram.append(f"    {comp}[{comp}]")
                elif type_ == "Service":
                    diagram.append(f"    {comp}(({comp}))")
                elif type_ == "Database":
                    diagram.append(f"    {comp}[(Database)]")
                elif type_ == "Cache":
                    diagram.append(f"    {comp}[(Cache)]")
                else:  # Other type
                    diagram.append(f"    {comp}[{comp}]")
            
            # Add relationships
            for rel in self.current_design["architecture"]["relationships"]:
                source, target = rel["relationship"].split("->")
                source = source.strip()
                target = target.strip()
                protocol = rel["protocol"]
                description = rel["description"]
                
                # Quote the description text
                label = f'"{protocol}: {description}"'
                
                if protocol == "HTTP":
                    diagram.append(f"    {source} -->|{label}| {target}")
                elif protocol == "gRPC":
                    diagram.append(f"    {source} -.->|{label}| {target}")
                elif protocol == "WebSocket":
                    diagram.append(f"    {source} ===|{label}| {target}")
                else:  # Other protocol
                    diagram.append(f"    {source} -->|{label}| {target}")
            
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

            # Format API sections
            internal_apis = "\n".join(f"- {api['endpoint']}" for api in self.current_design['apis']['internal'])
            external_apis = "\n".join(f"- {api['endpoint']}" for api in self.current_design['apis']['external'])
            
            # Format workflow section
            workflows = []
            for workflow in self.current_design['workflows']:
                workflows.append(f"- {workflow['api']}")
                workflows.append(f"  Requirement: {workflow['requirement']}")
                for step in workflow['steps']:
                    workflows.append(f"  {step['step']}")
                    for substep in step['substeps']:
                        workflows.append(f"    - {substep}")
            workflows_str = "\n".join(workflows)

            # Format components section
            components = []
            if "architecture" in self.current_design:
                for comp, type_ in self.current_design["architecture"]["component_types"].items():
                    components.append(f"- {comp}: {type_}")
            components_str = "\n".join(components)

            # Format optimizations section
            optimizations = []
            if "optimizations" in self.current_design:
                for opt in self.current_design["optimizations"]:
                    optimizations.append(f"- {opt}")
            optimizations_str = "\n".join(optimizations)

            # Format edge cases section
            edge_cases = []
            if "edge_cases" in self.current_design:
                if "edge_cases" in self.current_design["edge_cases"]:
                    edge_cases.append("### General Edge Cases")
                    for case in self.current_design["edge_cases"]["edge_cases"]:
                        edge_cases.append(f"- {case}")
                
                if "small_scale" in self.current_design["edge_cases"]:
                    edge_cases.append("\n### Small Scale Failures")
                    for failure in self.current_design["edge_cases"]["small_scale"]:
                        edge_cases.append(f"- {failure['failure']}")
                        for mitigation in failure['mitigation']:
                            edge_cases.append(f"  - {mitigation}")
                
                if "large_scale" in self.current_design["edge_cases"]:
                    edge_cases.append("\n### Large Scale Failures")
                    for failure in self.current_design["edge_cases"]["large_scale"]:
                        edge_cases.append(f"- {failure['failure']}")
                        for mitigation in failure['mitigation']:
                            edge_cases.append(f"  - {mitigation}")
            edge_cases_str = "\n".join(edge_cases)

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
{internal_apis}

### External
{external_apis}

## Workflows
{workflows_str}

## Components
{components_str}

## System Architecture
```mermaid
{mermaid_diagram}
```

## Optimizations
{optimizations_str}

## Edge Cases
{edge_cases_str}
"""

            with open(filename, 'w') as f:
                f.write(report)

            self.console.print(f"\n[green]Report generated successfully![/green]")
            self.console.print(f"File saved as: {filename}")
            self.console.print("\n[bold]Report Preview:[/bold]")
            self.console.print(Markdown(report))
        except Exception as e:
            self.console.print(f"[red]Error generating report: {str(e)}[/red]")

def main():
    parser = argparse.ArgumentParser(description='System Design Practice Tool')
    parser.add_argument('--start-step', type=int, default=1,
                      help='Start from a specific step (1-6) using stub data')
    args = parser.parse_args()
    
    practice = SystemDesignPractice()
    practice.start(args.start_step)

if __name__ == "__main__":
    main() 