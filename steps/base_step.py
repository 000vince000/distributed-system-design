from rich.console import Console
from rich.prompt import Prompt
from .helpers import InputHelper, DisplayHelper, StepNavigationHelper

class BaseStep:
    def __init__(self, console=None):
        self.console = console or Console()
        self.prompt = Prompt()
        # Initialize helpers
        self.input_helper = InputHelper(self.console, self.prompt)
        self.display_helper = DisplayHelper(self.console)
        self.navigation_helper = StepNavigationHelper(self.console, self.prompt)
    
    def execute(self, design_data):
        """Execute the step and return updated design data."""
        raise NotImplementedError("Subclasses must implement execute()") 