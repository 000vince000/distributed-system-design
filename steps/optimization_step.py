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
                    "6": "Loose coupling",
                    "7": "Other"
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
                    "7": "Idempotent operations",
                    "8": "Other"
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
                    "12": "DB materialized view",
                    "13": "Other"
                }
            },
            "4": {
                "name": "User Experience",
                "options": {
                    "1": "Client browser caching",
                    "2": "Cookies",
                    "3": "Lazy load",
                    "4": "Realtime notification",
                    "5": "Other"
                }
            },
            "5": {
                "name": "Reliability",
                "options": {
                    "1": "Rate limits with backoff",
                    "2": "Multiple availability zones",
                    "3": "Service failure detection & auto failover",
                    "4": "Circuit breaker",
                    "5": "Message delivery failure recovery",
                    "6": "Use different hash keys for cache and db",
                    "7": "Use safe deployment practice",
                    "8": "Replicate storage",
                    "9": "Use bulkheads for resource isolation",
                    "10": "Other"
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
            "reliability": "5",
            "disaster recovery": "5",
            "fault tolerance": "5",
            "resilience": "5",
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

    def _get_category_for_nfr(self, nfr):
        """Map NFR to optimization category."""
        nfr_lower = nfr.strip().lower()
        cat_key = self.nfr_to_cat.get(nfr_lower)
        
        # Smart matching if exact match not found
        if not cat_key:
            for key in self.nfr_to_cat:
                if key in nfr_lower or nfr_lower in key:
                    cat_key = self.nfr_to_cat[key]
                    break
        
        self.console.print(f"[dim]Debug: NFR '{nfr}' -> cat_key '{cat_key}'[/dim]")
        return cat_key

    def _select_category_manually(self):
        """Let user manually select optimization category."""
        self.console.print("\n[bold]Select optimization category:[/bold]")
        for key, value in self.optimization_options.items():
            self.console.print(f"{key}. {value['name']}")
        return self.input_helper.get_choice(
            "Select category",
            choices=list(self.optimization_options.keys())
        )

    def _process_subcategory(self, nfr, cat, subcat):
        """Process a single subcategory optimization."""
        self.console.print(f"[dim]You selected: {subcat}[/dim]")
        # Get optimization details
        details = self.input_helper.get_multi_line_input(
            "Enter optimization details (one per line, x to finish):"
        )
        # Combine multiple lines into a single explanation
        explanation = " ".join(details)
        
        # Get trade-offs
        tradeoffs = self.input_helper.get_multi_line_input(
            "Enter trade-offs for this subcategory (one per line, x to finish):"
        )
        tradeoff = " ".join(tradeoffs)
        
        return {
            "nfr": nfr,
            "category": cat["name"],
            "subcategory": subcat,
            "explanation": explanation,
            "tradeoffs": tradeoff
        }

    def _process_free_text_optimization(self, nfr):
        """Process free text optimization when no category is found."""
        self.console.print("[dim]Suggestions: Scalability, Consistency, Efficiency, User Experience, etc.[/dim]")
        req_optimizations = self.input_helper.get_multi_line_input(
            "Enter optimizations (one per line, x to finish):"
        )
        return [{
            "nfr": nfr,
            "category": "Other",
            "subcategory": "Free text",
            "explanation": opt,
            "tradeoffs": ""
        } for opt in req_optimizations]

    def _process_nfr(self, nfr):
        """Process a single NFR optimization."""
        cat_key = self._get_category_for_nfr(nfr)
        
        if not cat_key:
            cat_key = self._select_category_manually()
        
        if cat_key and cat_key in self.optimization_options:
            cat = self.optimization_options[cat_key]
            optimizations = []
            
            while True:
                self.console.print(f"[bold]Select subcategory for {nfr}:[/bold]")
                self.display_helper.display_list(cat["options"].values(), enumerate_items=True)
                self.console.print("x. Done with this NFR")
                
                subcat_choices = list(cat["options"].keys()) + [self.input_helper.SKIP_CHOICE]
                subcat_selected = self.input_helper.get_choice(
                    "Select subcategory",
                    choices=subcat_choices
                )
                
                if subcat_selected == self.input_helper.SKIP_CHOICE:
                    break
                    
                subcat = cat["options"][subcat_selected]
                optimizations.append(self._process_subcategory(nfr, cat, subcat))
            
            return optimizations
        else:
            return self._process_free_text_optimization(nfr)

    def execute(self, design_data):
        """Add design optimizations."""
        self.navigation_helper.display_step_header(5)
        
        # Initialize optimizations list
        all_optimizations = []
        
        # Get non-functional requirements
        nonfunctional_reqs = design_data["requirements"]["nonfunctional"]
        if not nonfunctional_reqs:
            self.console.print("[yellow]No non-functional requirements defined. Please define requirements first.[/yellow]")
            return design_data
        
        # Process each NFR
        remaining_nfrs = nonfunctional_reqs.copy()
        while remaining_nfrs:
            # Display remaining NFRs for selection
            self.console.print("\n[bold]Select NFR(s) to optimize for this component:[/bold]")
            self.display_helper.display_list(remaining_nfrs, enumerate_items=True)
            self.console.print("x. Done with all NFRs")
            
            nfr_choices = [str(i) for i in range(1, len(remaining_nfrs) + 1)] + [self.input_helper.SKIP_CHOICE]
            nfr_selected = self.input_helper.get_choice(
                "Select NFR",
                choices=nfr_choices
            )
            
            if nfr_selected == self.input_helper.SKIP_CHOICE:
                break
            
            nfr = remaining_nfrs[int(nfr_selected) - 1]
            self.console.print(f"\n[bold]Optimizing for NFR: {nfr}[/bold]")
            
            # Process the selected NFR
            optimizations = self._process_nfr(nfr)
            all_optimizations.extend(optimizations)
            
            # Remove processed NFR
            remaining_nfrs.pop(int(nfr_selected) - 1)
        
        # Store optimizations in structured format
        design_data["optimizations"] = {
            "items": all_optimizations,
            "summary": [f"{opt['nfr']} / {opt['subcategory']}: {opt['explanation']}" for opt in all_optimizations]
        }
        return design_data 