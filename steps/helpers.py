from rich.console import Console
from rich.prompt import Prompt

class InputHelper:
    def __init__(self, console: Console, prompt: Prompt):
        self.console = console
        self.prompt = prompt
    
    def get_multi_line_input(self, prompt: str, terminator: str = "x") -> list:
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
    
    def get_choice(self, prompt: str, choices: list, default: str = None) -> str:
        """Get a choice from a list of options."""
        prompt_kwargs = {
            "prompt": prompt,
            "choices": choices
        }
        if default and len(choices) == 1:
            prompt_kwargs["default"] = default
        return self.prompt.ask(**prompt_kwargs)

class DisplayHelper:
    def __init__(self, console: Console):
        self.console = console
    
    def display_list(self, items: list, prefix: str = "-", enumerate_items: bool = False):
        """Display a list of items with a prefix.
        
        Args:
            items: List of items to display
            prefix: Prefix to use for each item
            enumerate_items: Whether to enumerate items (1-based)
        """
        for i, item in enumerate(items, 1):
            if enumerate_items:
                self.console.print(f"{i}. {item}")
            else:
                self.console.print(f"{prefix} {item}")
    
    def display_nested_list(self, items: list, prefix: str = "-", indent: str = "  "):
        """Display a nested list of items with indentation."""
        for item in items:
            if isinstance(item, dict):
                self.console.print(f"{prefix} {item['name']}")
                for subitem in item.get('items', []):
                    self.console.print(f"{indent}{prefix} {subitem}")
            else:
                self.console.print(f"{prefix} {item}")

class StepNavigationHelper:
    def __init__(self, console: Console, prompt: Prompt):
        self.console = console
        self.prompt = prompt
        self.step_names = {
            1: "Requirements",
            2: "APIs",
            3: "Workflows",
            4: "Architecture",
            5: "Optimizations",
            6: "Edge Cases"
        }
    
    def display_step_header(self, step_number: int):
        """Display the header for a step."""
        self.console.print(f"\n[bold]Step {step_number}: {self.step_names[step_number]}[/bold]")
    
    def ask_continue(self) -> bool:
        """Ask if user wants to continue to next step."""
        return self.prompt.ask(
            "\nContinue to next step?",
            choices=["y", "n"],
            default="y"
        ) == "y" 