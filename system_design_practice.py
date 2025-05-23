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
                mermaid_diagram = architecture_step.diagram_generator.generate_mermaid_diagram(self.current_design)
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

    def _load_design_file(self, filename: str, is_stub: bool = False) -> int:
        """Load design data from a file and return the next step number.
        
        Args:
            filename: Path to the file to load
            is_stub: Whether this is a stub file (True) or partial file (False)
            
        Returns:
            int: The step number to start from
        """
        try:
            if is_stub:
                # For stubs, the step number comes from the command line
                # and we load the corresponding stub data
                step = int(filename)  # filename is actually the step number for stubs
                if step == 2:
                    self.current_design = get_step1_stub()
                elif step == 3:
                    self.current_design = get_step2_stub()
                elif step == 4:
                    self.current_design = get_step3_stub()
                elif step == 5:
                    self.current_design = get_step4_stub()
                elif step == 6:
                    self.current_design = get_step5_stub()
                return step
            else:
                # For partial files, load the data and get next step from file
                with open(filename, 'r') as f:
                    data = json.load(f)
                    self.current_design = data['design']
                    self.start_time = data['start_time']
                    return data['step'] + 1  # Return the next step
        except Exception as e:
            self.console.print(f"[red]Error loading design file: {str(e)}[/red]")
            return 1

    def start(self, filename: str, is_stub: bool = False):
        """Start or resume the system design practice session.
        
        Args:
            filename: For stubs, this is the step number. For partial files, this is the file path.
            is_stub: Whether we're loading a stub file (True) or partial file (False)
        """
        self.console.print(Panel.fit("System Design Practice Tool"))
        
        # Load the design file and get the starting step
        start_step = self._load_design_file(filename, is_stub)
        
        # Select design question if not already set
        if not self.current_design["question"]:
            self.select_design_question(start_step)
                    
        # Display summary of previous steps
        self.console.print(f"\n{'Starting' if is_stub else 'Resuming'} from Step {start_step}\n")
        self.console.print("Previous Steps Summary:\n")
        
        # Display summaries of completed steps
        for step in range(1, start_step):
            self._display_stub_summary(step)
        
        # Execute remaining steps
        for i, step in enumerate(self.steps[start_step - 1:], start_step):
            self.current_design = step.execute(self.current_design)
            self._save_partial_design(i)
            
            # Ask if user wants to continue
            if i < len(self.steps):
                continue_choice = self.prompt.ask(
                    "\nContinue to next step?",
                    choices=["y", "n"],
                    default="y"
                )
                if continue_choice == "n":
                    break
        
        # Generate final report
        self.generate_report()

    def _save_partial_design(self, step_number: int):
        """Save partial design after completing a step."""
        if not hasattr(self, 'start_time') or self.start_time is None:
            return  # Don't save if using stubs
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Get question filename from the first line of the question
        question_first_line = self.current_design['question'].split('\n')[0].lower()
        question_name = ''.join(c if c.isalnum() or c.isspace() else '' for c in question_first_line)
        question_name = question_name.replace(' ', '_')
        question_name = question_name[:30]  # Shorter max length
        
        # Delete any existing partial files for this question
        try:
            for filename in os.listdir("design_reports"):
                if filename.startswith(f"partial_{question_name}_") and filename.endswith(".json"):
                    filepath = os.path.join("design_reports", filename)
                    os.remove(filepath)
                    self.console.print(f"[yellow]Deleted old partial file: {filename}[/yellow]")
        except Exception as e:
            self.console.print(f"[yellow]Warning: Could not clean up old partial files: {str(e)}[/yellow]")
        
        # Save new partial file
        filename = f"design_reports/partial_{question_name}_step{step_number}_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump({
                'step': step_number,
                'design': self.current_design,
                'start_time': self.start_time
            }, f, indent=2)
        
        self.console.print(f"\n[yellow]Partial design saved to: {filename}[/yellow]")

    def _cleanup_partial_files(self, question_name: str):
        """Clean up partial files for the current design."""
        try:
            question_name = question_name.lower()
            question_name = ''.join(c if c.isalnum() or c.isspace() else '' for c in question_name)
            question_name = question_name.replace(' ', '_')
            question_name = question_name[:50]
            
            for filename in os.listdir("design_reports"):
                if filename.startswith(f"partial_design_{question_name}_") and filename.endswith(".json"):
                    os.remove(os.path.join("design_reports", filename))
        except Exception as e:
            self.console.print(f"[yellow]Warning: Could not clean up partial files: {str(e)}[/yellow]")

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
            
            # Initialize start time when starting a new design
            self.start_time = time.time()
        
        # Execute steps starting from the specified step
        for i, step in enumerate(self.steps[start_step-1:], start=start_step):
            self.current_design = step.execute(self.current_design)
            # Save partial design after each step
            self._save_partial_design(i)
        
        # Clean up partial files after generating final report
        self._cleanup_partial_files(self.current_design["question"])
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

    def _format_edge_case_section(self, section_title, items, is_failure=False):
        lines = [f"### {section_title}"]
        for item in items:
            name = item['failure'] if is_failure else item['edge_case']
            lines.append(f"- {name}")
            if item.get('prevention'):
                lines.append(f"  - Prevention:")
                for p in item['prevention']:
                    lines.append(f"    - {p}")
            if item.get('mitigation'):
                lines.append(f"  - Mitigation:")
                for m in item['mitigation']:
                    lines.append(f"    - {m}")
        return '\n'.join(lines)

    def generate_report(self):
        """Generate the final report."""
        try:
            elapsed_time = time.time() - self.start_time
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create design_reports directory if it doesn't exist
            os.makedirs("design_reports", exist_ok=True)
            
            # Create a more descriptive filename from the question
            question_name = self.current_design['question'].lower()
            # Remove special characters and replace spaces with underscores
            question_name = ''.join(c if c.isalnum() or c.isspace() else '' for c in question_name)
            question_name = question_name.replace(' ', '_')
            # Truncate if too long
            question_name = question_name[:50]
            
            filename = f"design_reports/design_report_{question_name}_{timestamp}.md"

            # Generate mermaid diagram
            mermaid_diagram = self.generate_mermaid_diagram()

            # Format API sections
            internal_apis = []
            for api in self.current_design['apis']['internal']:
                internal_apis.append(f"- {api['endpoint']}")
                if api['request']:
                    internal_apis.append(f"  - Request: {', '.join(api['request'])}")
                if api['response']:
                    internal_apis.append(f"  - Response: {', '.join(api['response'])}")
            
            external_apis = []
            for api in self.current_design['apis']['external']:
                external_apis.append(f"- {api['endpoint']}")
                if api['request']:
                    external_apis.append(f"  - Request: {', '.join(api['request'])}")
                if api['response']:
                    external_apis.append(f"  - Response: {', '.join(api['response'])}")
            
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

            # Format database schema section
            database_schema = []
            if "architecture" in self.current_design and "database_schema" in self.current_design["architecture"]:
                for schema in self.current_design["architecture"]["database_schema"]:
                    database_schema.append(f"- {schema}")
            database_schema_str = "\n".join(database_schema)

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
                    edge_cases.append(self._format_edge_case_section(
                        "General Edge Cases",
                        self.current_design["edge_cases"]["edge_cases"],
                        is_failure=False
                    ))
                if "small_scale" in self.current_design["edge_cases"]:
                    edge_cases.append(self._format_edge_case_section(
                        "Small Scale Failures",
                        self.current_design["edge_cases"]["small_scale"],
                        is_failure=True
                    ))
                if "large_scale" in self.current_design["edge_cases"]:
                    edge_cases.append(self._format_edge_case_section(
                        "Large Scale Failures",
                        self.current_design["edge_cases"]["large_scale"],
                        is_failure=True
                    ))
            edge_cases_str = "\n\n".join(edge_cases)

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
{chr(10).join(internal_apis)}

### External
{chr(10).join(external_apis)}

## Workflows
{workflows_str}

## Components
{components_str}

## System Architecture
```mermaid
{mermaid_diagram}
```

## Database Schema
{database_schema_str}

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
    parser.add_argument('--load-partial', type=str,
                      help='Load a partial design file to resume from')
    args = parser.parse_args()
    
    practice = SystemDesignPractice()
    
    if args.load_partial:
        practice.start(args.load_partial, is_stub=False)
    else:
        practice.start(str(args.start_step), is_stub=True)

if __name__ == "__main__":
    main() 