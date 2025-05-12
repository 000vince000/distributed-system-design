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
                    "5": "Read replica",
                    "6": "Loose coupling"
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
                    "6": "Token leasing",
                    "7": "Idempotent operations"
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
        nfrs = design_data["requirements"].get("nonfunctional", [])
        nfr_to_cat = {
            # Scalability/Availability
            "scalability": "1",
            "high availability": "1",
            "availability": "1",
            "fault tolerance": "1",
            "resilience": "1",
            "reliability": "1",
            "disaster recovery": "1",
            # Consistency
            "consistency": "2",
            "data consistency": "2",
            "strong consistency": "2",
            "eventual consistency": "2",
            "read-after-write consistency": "2",
            # Efficiency/Performance
            "efficiency": "3",
            "performance": "3",
            "low latency": "3",
            "throughput": "3",
            "resource utilization": "3",
            "cost efficiency": "3",
            # User Experience
            "user experience": "4",
            "ux": "4",
            "responsiveness": "4",
            "usability": "4",
            "realtime": "4",
            # Add more as needed
        }
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
            component = remaining_components[int(choice) - 1]
            self.console.print(f"\n[bold]Optimizing component: {component}[/bold]")
            # NFR selection
            if not nfrs:
                self.console.print("[yellow]No non-functional requirements defined. Please define requirements first.[/yellow]")
                break
            self.console.print("\n[bold]Select NFR(s) to optimize for this component:[/bold]")
            for i, nfr in enumerate(nfrs, 1):
                self.console.print(f"{i}. {nfr}")
            self.console.print(f"x. Done")
            nfr_choices = [str(i) for i in range(1, len(nfrs) + 1)] + ["x"]
            nfr_prompt_kwargs = {
                "prompt": "Select NFR(s) (comma-separated numbers, or 'x' to finish):",
                "choices": nfr_choices
            }
            if len(nfr_choices) == 2:  # Only one NFR + 'x'
                nfr_prompt_kwargs["default"] = nfr_choices[0]
            nfr_selected = self.prompt.ask(**nfr_prompt_kwargs)
            if nfr_selected == "x":
                remaining_components.remove(component)
                continue
            nfr_indices = [int(x.strip()) for x in nfr_selected.split(",") if x.strip().isdigit() and 1 <= int(x.strip()) <= len(nfrs)]
            selected_nfrs = [nfrs[i-1] for i in nfr_indices]
            component_optimizations = []
            for nfr in selected_nfrs:
                self.console.print(f"\n[bold]Optimizing for NFR: {nfr}[/bold]")
                # Try to map NFR to a category
                cat_key = nfr_to_cat.get(nfr.strip().lower())
                if cat_key and cat_key in self.optimization_options:
                    cat = self.optimization_options[cat_key]
                    self.console.print(f"[bold]Select subcategory(ies) for {nfr} (comma-separated numbers):[/bold]")
                    for k, v in cat["options"].items():
                        self.console.print(f"{k}. {v}")
                    subcat_choices = list(cat["options"].keys()) + ["x"]
                    subcat_prompt_kwargs = {
                        "prompt": f"Select subcategory(ies) (comma-separated numbers, or 'x' to skip):",
                        "choices": subcat_choices
                    }
                    subcat_selected = self.prompt.ask(**subcat_prompt_kwargs)
                    if subcat_selected.strip().lower() == "x":
                        continue
                    subcat_indices = [x.strip() for x in subcat_selected.split(",") if x.strip() in cat["options"]]
                    for idx in subcat_indices:
                        subcat = cat["options"][idx]
                        self.console.print(f"[dim]You selected: {subcat}[/dim]")
                        # Prompt for free-text details for this subcategory
                        details = self._get_multi_line_input(
                            f"Enter details for {subcat} (one per line, x to finish):",
                            "x"
                        )
                        for detail in details:
                            component_optimizations.append(f"{nfr} / {subcat}: {detail}")
                else:
                    # No mapped subcategory, just prompt for free text
                    self.console.print("[dim]Suggestions: Scalability, Consistency, Efficiency, User Experience, etc.[/dim]")
                    nfr_opts = self._get_multi_line_input(
                        "Enter optimizations (one per line, x to finish):",
                        "x"
                    )
                    for opt in nfr_opts:
                        component_optimizations.append(f"{nfr}: {opt}")
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