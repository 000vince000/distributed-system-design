from rich.console import Console
from rich.markup import escape
from rich.prompt import Prompt
from rich.rule import Rule
from rich.theme import Theme

# Centralized color palette. Use these semantic names (e.g. "[warning]...")
# in console.print calls instead of raw color names, so the look can be
# retuned in one place.
APP_THEME = Theme({
    "warning": "yellow",
    "success": "green",
    "error": "bold red",
    "muted": "dim",
    "info": "blue",
    "header": "bold cyan",
})


class QuitRequested(Exception):
    """Raised when the user chooses to gracefully exit via the quit option."""
    pass


def parse_human_number(s: str):
    """Parse a string like '10M', '3.5k', '500' into a float. Returns None if unparseable."""
    if not s:
        return None
    s = s.strip().upper().replace(",", "").replace("_", "")
    suffixes = {"K": 1e3, "M": 1e6, "B": 1e9}
    multiplier = 1
    if s and s[-1] in suffixes:
        multiplier = suffixes[s[-1]]
        s = s[:-1]
    try:
        return float(s) * multiplier
    except ValueError:
        return None


def format_human_number(n: float) -> str:
    """Format a number using K/M/B suffixes, e.g. 1500 -> '1.5K'."""
    for suffix, threshold in (("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(n) >= threshold:
            value = n / threshold
            return f"{value:.2f}".rstrip("0").rstrip(".") + suffix
    return f"{n:.2f}".rstrip("0").rstrip(".")


class InputHelper:
    def __init__(self, console: Console, prompt: Prompt):
        self.console = console
        self.prompt = prompt
        self.SKIP_CHOICE = "x"  # Standard skip/finish choice
        self.QUIT_CHOICE = "q"  # Standard graceful-exit choice
        self.UNDO_CHOICE = "u"  # Undo last entered line, in get_multi_line_input

    def get_line_input(self, prompt: str, default: str = "") -> str:
        """Get a single line of free-text input.

        Args:
            prompt: The prompt to display
            default: Value to use if the user just presses enter
        """
        suffix = f" [{default}]" if default else ""
        self.console.print(f"\n{prompt}{suffix} (or '{self.QUIT_CHOICE}' to quit)")
        line = input()
        stripped = line.strip()
        if stripped == self.QUIT_CHOICE:
            raise QuitRequested()
        return stripped if stripped else default

    def get_multi_line_input(self, prompt: str, existing: list = None) -> list:
        """Get multi-line input from user until a blank line is entered.

        Args:
            prompt: The prompt to display
            existing: Previously entered lines to pre-load, e.g. when resuming
                a step that was interrupted mid-way. Shown to the user and
                stays editable via undo.
        """
        self.console.print(f"\n{prompt} (or '{self.QUIT_CHOICE}' to quit, '{self.UNDO_CHOICE}' to undo last line)")
        lines = list(existing) if existing else []
        if lines:
            self.console.print("[muted]Already entered:[/muted]")
            for line in lines:
                self.console.print(f"  - {line}")
        while True:
            line = input()
            stripped = line.strip()
            if stripped == self.QUIT_CHOICE:
                raise QuitRequested()
            if stripped == self.UNDO_CHOICE:
                if lines:
                    removed = lines.pop()
                    self.console.print(f"[warning]Removed: {removed}[/warning]")
                else:
                    self.console.print("[warning]Nothing to undo.[/warning]")
                continue
            if not stripped:  # Blank line finishes input
                break
            lines.append(stripped)
        return lines

    def get_choice(self, prompt: str, choices: list, default: str = None, skip_prompt: bool = False,
                   show_choices: bool = True) -> str:
        """Get a choice from a list of options.

        Args:
            prompt: The prompt to display
            choices: List of valid choices
            default: Default choice if only one option
            skip_prompt: Whether to add skip option to prompt
            show_choices: Whether to echo the choice list in brackets after the
                prompt. Set to False when the choices were already displayed
                as a numbered list just above, to avoid showing them twice.
        """
        # Add skip choice if not present and skip_prompt is True
        if skip_prompt and self.SKIP_CHOICE not in choices:
            choices = choices + [self.SKIP_CHOICE]

        # Add quit choice if not already present
        if self.QUIT_CHOICE not in choices:
            choices = choices + [self.QUIT_CHOICE]

        hints = []
        if skip_prompt:
            hints.append(f"'{self.SKIP_CHOICE}' to skip")
        hints.append(f"'{self.QUIT_CHOICE}' to quit")

        prompt_kwargs = {
            "prompt": prompt + f" (or {', '.join(hints)})",
            "choices": choices,
            "show_choices": show_choices
        }
        if default and len(choices) == 1:
            prompt_kwargs["default"] = default
        choice = self.prompt.ask(**prompt_kwargs)
        if choice == self.QUIT_CHOICE:
            raise QuitRequested()
        return choice

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
                self.console.print(f"{i}. {escape(item)}")
            else:
                self.console.print(f"{prefix} {escape(item)}")
    
    def display_nested_list(self, items: list, prefix: str = "-", indent: str = "  "):
        """Display a nested list of items with indentation."""
        for item in items:
            if isinstance(item, dict):
                self.console.print(f"{prefix} {escape(item['name'])}")
                for subitem in item.get('items', []):
                    self.console.print(f"{indent}{prefix} {escape(subitem)}")
            else:
                self.console.print(f"{prefix} {escape(item)}")

class StepNavigationHelper:
    def __init__(self, console: Console, prompt: Prompt):
        self.console = console
        self.prompt = prompt
        self.step_names = {
            1: "Requirements",
            2: "Capacity Estimation",
            3: "APIs",
            4: "Workflows",
            5: "Architecture",
            6: "Optimizations",
            7: "Edge Cases"
        }
    
    def display_step_header(self, step_number: int):
        """Display the header for a step."""
        self.console.print()
        self.console.print(Rule(f"Step {step_number}: {self.step_names[step_number]}", style="header"))
    
    def ask_continue(self) -> bool:
        """Ask if user wants to continue to next step."""
        choice = self.prompt.ask(
            "\nContinue to next step? (or 'q' to quit)",
            choices=["y", "n", "q"],
            default="y"
        )
        if choice == "q":
            raise QuitRequested()
        return choice == "y"