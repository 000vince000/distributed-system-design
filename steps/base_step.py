from rich.console import Console
from rich.prompt import Prompt

class BaseStep:
    def __init__(self, console=None):
        self.console = console or Console()
        self.prompt = Prompt()
    
    def _get_multi_line_input(self, prompt: str, terminator: str = "") -> list:
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
    
    def execute(self, design_data):
        """Execute the step and return updated design data."""
        raise NotImplementedError("Subclasses must implement execute()") 