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
        
        # Define NFR to category mapping
        self.nfr_to_cat = {
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
            "consistent": "2",
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
            "realtime": "4"
        }

    def execute(self, design_data):
        """Add design optimizations."""
        self.console.print("\n[bold]Step 5: Design Optimization[/bold]")
        
        # Initialize optimizations list
        optimizations = []
        
        # Get non-functional requirements
        nonfunctional_reqs = design_data["requirements"]["nonfunctional"]
        if not nonfunctional_reqs:
            self.console.print("[yellow]No non-functional requirements defined. Please define requirements first.[/yellow]")
            return design_data
            
        # Display non-functional requirements for selection
        self.console.print("\n[bold]Select NFR(s) to optimize for this component:[/bold]")
        for i, nfr in enumerate(nonfunctional_reqs, 1):
            self.console.print(f"{i}. {nfr}")
        self.console.print("x. Done")
        
        nfr_choices = [str(i) for i in range(1, len(nonfunctional_reqs) + 1)] + ["x"]
        nfr_selected = self.prompt.ask(
            "Select NFR (or 'x' to finish):",
            choices=nfr_choices
        )
        
        if nfr_selected == "x":
            return design_data
        
        nfr = nonfunctional_reqs[int(nfr_selected) - 1]
        self.console.print(f"\n[bold]Optimizing for NFR: {nfr}[/bold]")
        
        # Try to map NFR to a category
        nfr_lower = nfr.strip().lower()
        cat_key = self.nfr_to_cat.get(nfr_lower)
        
        # Smart matching if exact match not found
        if not cat_key:
            for key in self.nfr_to_cat:
                if key in nfr_lower or nfr_lower in key:
                    cat_key = self.nfr_to_cat[key]
                    break
        
        self.console.print(f"[dim]Debug: NFR '{nfr}' -> cat_key '{cat_key}'[/dim]")
        
        if not cat_key:
            # If no match found, let user select category
            self.console.print("\n[bold]Select optimization category:[/bold]")
            for key, value in self.optimization_options.items():
                self.console.print(f"{key}. {value['name']}")
            cat_key = self.prompt.ask("Select category:", choices=list(self.optimization_options.keys()))
        
        if cat_key and cat_key in self.optimization_options:
            cat = self.optimization_options[cat_key]
            self.console.print(f"[bold]Select subcategory for {nfr}:[/bold]")
            for k, v in cat["options"].items():
                self.console.print(f"{k}. {v}")
            self.console.print("x. Skip")
            
            subcat_choices = list(cat["options"].keys()) + ["x"]
            subcat_selected = self.prompt.ask(
                "Select subcategory (or 'x' to skip):",
                choices=subcat_choices
            )
            
            if subcat_selected != "x":
                subcat = cat["options"][subcat_selected]
                self.console.print(f"[dim]You selected: {subcat}[/dim]")
                # Prompt for free-text details for this subcategory
                details = self._get_multi_line_input(
                    f"Enter details for {subcat} (one per line, x to finish):",
                    "x"
                )
                # Combine multiple lines into a single explanation
                explanation = " ".join(details)
                optimizations.append(f"{nfr} / {subcat}: {explanation}")
                # Prompt for trade-offs for this subcategory
                tradeoffs = self._get_multi_line_input(
                    f"Enter trade-offs for {subcat} (one per line, x to finish):",
                    "x"
                )
                # Combine multiple lines into a single trade-offs consideration
                tradeoff = " ".join(tradeoffs)
                optimizations.append(f"{nfr} / {subcat} / Trade-offs: {tradeoff}")
        else:
            # No mapped subcategory, just prompt for free text
            self.console.print("[dim]Suggestions: Scalability, Consistency, Efficiency, User Experience, etc.[/dim]")
            req_optimizations = self._get_multi_line_input(
                "Enter optimizations (one per line, x to finish):",
                "x"
            )
            optimizations = [f"{nfr}: {opt}" for opt in req_optimizations]
        
        design_data["optimizations"] = optimizations
        return design_data 