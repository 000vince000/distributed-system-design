from .base_step import BaseStep

class OptimizationStep(BaseStep):
    def __init__(self, console=None):
        super().__init__(console)
        # Define optimization options
        self.optimization_options = {
            "1": {
                "name": "Scalability",
                "options": {
                    "1": "Vertical scaling",
                    "2": "Horizontal scaling",
                    "3": "Sharding",
                    "4": "Async processing",
                    "5": "Read replica"
                }
            },
            "2": {
                "name": "Consistency",
                "options": {
                    "1": "Quorum",
                    "2": "Write-through cache",
                    "3": "Distributed lock",
                    "4": "ACID compliant storage",
                    "5": "FIFO queue",
                    "6": "Token leasing"
                }
            },
            "3": {
                "name": "Efficiency",
                "options": {
                    "1": "Transport data compression",
                    "2": "Pre-upload transport data",
                    "3": "CDN",
                    "4": "Use UDP instead of TCP",
                    "5": "Load balancing",
                    "6": "Caching",
                    "7": "Worker parallelism",
                    "8": "DB indexing",
                    "9": "NoSQL DB",
                    "10": "DB read replica",
                    "11": "DB connection pooler",
                    "12": "DB materialized view"
                }
            },
            "4": {
                "name": "User Experience",
                "options": {
                    "1": "Client browser caching",
                    "2": "Cookies",
                    "3": "Lazy load",
                    "4": "Realtime notification"
                }
            }
        }

    def _get_components(self, design_data):
        """Extract unique components from workflows."""
        components = set()
        for workflow in design_data.get("workflows", []):
            for step in workflow["steps"]:
                components.add(step["step"].strip())
        return sorted(list(components))

    def _select_optimization_category(self):
        """Let user select optimization category."""
        self.console.print("\n[bold]Select optimization category:[/bold]")
        for key, value in self.optimization_options.items():
            self.console.print(f"{key}/ {value['name']}")
        self.console.print("x/ Done")
        
        choices = list(self.optimization_options.keys()) + ["x"]
        return self.prompt.ask("Select category:", choices=choices)

    def _select_optimization_options(self, category):
        """Let user select specific optimization options for a category."""
        options = self.optimization_options[category]["options"]
        self.console.print(f"\n[bold]Select {self.optimization_options[category]['name']} optimizations:[/bold]")
        for key, value in options.items():
            self.console.print(f"{category}.{key}/ {value}")
        
        choices = list(options.keys())
        selected = self.prompt.ask(
            "Select options (comma-separated numbers):",
            choices=choices
        )
        
        selected_indices = [x.strip() for x in selected.split(",")]
        return [options[idx] for idx in selected_indices if idx in options]

    def execute(self, design_data):
        """Add design optimizations."""
        self.console.print("\n[bold]Step 5: Design Optimization[/bold]")
        
        # Get components from workflows
        components = self._get_components(design_data)
        if not components:
            self.console.print("[yellow]No components found in workflows. Please define workflows first.[/yellow]")
            return design_data
        
        # Store all optimizations
        all_optimizations = []
        remaining_components = components.copy()
        
        while remaining_components:
            # Show remaining components
            self.console.print("\n[bold]Remaining components to optimize:[/bold]")
            for i, comp in enumerate(remaining_components, 1):
                self.console.print(f"{i}. {comp}")
            
            # Let user select a component
            choices = [str(i) for i in range(1, len(remaining_components) + 1)]
            prompt_kwargs = {
                "prompt": "Select a component to optimize:",
                "choices": choices
            }
            if len(choices) == 1:
                prompt_kwargs["default"] = choices[0]
            choice = self.prompt.ask(**prompt_kwargs)
            
            # Get the selected component
            component = remaining_components[int(choice) - 1]
            self.console.print(f"\n[bold]Optimizing component: {component}[/bold]")
            
            # Get optimizations for this component
            component_optimizations = []
            while True:
                # Category selection
                cat_choices = list(self.optimization_options.keys()) + ["x"]
                cat_prompt_kwargs = {
                    "prompt": "Select optimization category:",
                    "choices": cat_choices
                }
                if len(cat_choices) == 2:  # Only one category + 'x'
                    cat_prompt_kwargs["default"] = cat_choices[0]
                category = self.prompt.ask(**cat_prompt_kwargs)
                if category == "x":
                    break
                # Option selection
                options = self.optimization_options[category]["options"]
                opt_choices = list(options.keys())
                opt_prompt_kwargs = {
                    "prompt": f"Select {self.optimization_options[category]['name']} optimizations:",
                    "choices": opt_choices
                }
                if len(opt_choices) == 1:
                    opt_prompt_kwargs["default"] = opt_choices[0]
                selected = self.prompt.ask(**opt_prompt_kwargs)
                selected_indices = [x.strip() for x in selected.split(",")]
                for idx in selected_indices:
                    if idx in options:
                        component_optimizations.append(f"{self.optimization_options[category]['name']}: {options[idx]}")
            
            if component_optimizations:
                all_optimizations.append(f"Component: {component}")
                all_optimizations.extend([f"  - {opt}" for opt in component_optimizations])
            
            # Remove the optimized component from remaining components
            remaining_components.remove(component)
            
            # Show current optimization summary
            if all_optimizations:
                self.console.print("\n[bold]Current Optimization Summary:[/bold]")
                for opt in all_optimizations:
                    self.console.print(opt)
        
        # Store optimizations in design data
        design_data["optimizations"] = all_optimizations
        
        # Display final summary
        if all_optimizations:
            self.console.print("\n[bold]Final Optimization Summary:[/bold]")
            for opt in all_optimizations:
                self.console.print(opt)
        
        return design_data 