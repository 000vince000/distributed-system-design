from .base_step import BaseStep
from config.optimization_config import OPTIMIZATION_OPTIONS, NFR_TO_CATEGORY

class OptimizationStep(BaseStep):
    def __init__(self, console=None):
        super().__init__(console)
        # Use configuration from config file
        self.optimization_options = OPTIMIZATION_OPTIONS
        self.nfr_to_cat = NFR_TO_CATEGORY

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
            remaining_options = list(cat["options"].items())  # Keep as (key, value) pairs
            
            while remaining_options:
                self.console.print(f"[bold]Select subcategory for {nfr}:[/bold]")
                self.display_helper.display_list([opt[1] for opt in remaining_options], enumerate_items=True)
                self.console.print("x. Done with this NFR")
                
                subcat_choices = [str(i) for i in range(1, len(remaining_options) + 1)] + [self.input_helper.SKIP_CHOICE]
                subcat_selected = self.input_helper.get_choice(
                    "Select subcategory",
                    choices=subcat_choices
                )
                
                if subcat_selected == self.input_helper.SKIP_CHOICE:
                    break
                
                # Get the selected option and remove it from remaining options
                selected_idx = int(subcat_selected) - 1
                selected_key, selected_value = remaining_options.pop(selected_idx)
                optimizations.append(self._process_subcategory(nfr, cat, selected_value))
            
            return optimizations
        else:
            return self._process_free_text_optimization(nfr)

    def execute(self, design_data):
        """Add design optimizations."""
        self.navigation_helper.display_step_header(5)
        
        # Initialize optimizations list with hierarchical structure
        all_optimizations = []
        nfr_optimizations = {}  # Temporary dict to group by NFR
        
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
            cat_key = self._get_category_for_nfr(nfr)
            if not cat_key:
                cat_key = self._select_category_manually()
            
            if cat_key and cat_key in self.optimization_options:
                cat = self.optimization_options[cat_key]
                optimizations = []
                remaining_options = list(cat["options"].items())
                
                while remaining_options:
                    self.console.print(f"[bold]Select subcategory for {nfr}:[/bold]")
                    self.display_helper.display_list([opt[1] for opt in remaining_options], enumerate_items=True)
                    self.console.print("x. Done with this NFR")
                    
                    subcat_choices = [str(i) for i in range(1, len(remaining_options) + 1)] + [self.input_helper.SKIP_CHOICE]
                    subcat_selected = self.input_helper.get_choice(
                        "Select subcategory",
                        choices=subcat_choices
                    )
                    
                    if subcat_selected == self.input_helper.SKIP_CHOICE:
                        break
                    
                    selected_idx = int(subcat_selected) - 1
                    selected_key, selected_value = remaining_options.pop(selected_idx)
                    
                    # Get optimization details
                    details = self.input_helper.get_multi_line_input(
                        "Enter optimization details (one per line, x to finish):"
                    )
                    explanation = " ".join(details)
                    
                    # Get trade-offs
                    tradeoffs = self.input_helper.get_multi_line_input(
                        "Enter trade-offs for this subcategory (one per line, x to finish):"
                    )
                    tradeoff = " ".join(tradeoffs)
                    
                    optimizations.append({
                        "subcategory": selected_value,
                        "explanation": explanation,
                        "tradeoffs": tradeoff
                    })
                
                # Store optimizations for this NFR
                nfr_optimizations[nfr] = {
                    "nfr": nfr,
                    "category": cat["name"],
                    "optimizations": optimizations
                }
            else:
                # Handle free text optimization
                req_optimizations = self.input_helper.get_multi_line_input(
                    "Enter optimizations (one per line, x to finish):"
                )
                nfr_optimizations[nfr] = {
                    "nfr": nfr,
                    "category": "Other",
                    "optimizations": [{
                        "subcategory": "Free text",
                        "explanation": opt,
                        "tradeoffs": ""
                    } for opt in req_optimizations]
                }
            
            # Remove processed NFR
            remaining_nfrs.pop(int(nfr_selected) - 1)
        
        # Convert dictionary to list for final storage
        all_optimizations = list(nfr_optimizations.values())
        
        # Store optimizations in structured format
        design_data["optimizations"] = {
            "items": all_optimizations
        }
        
        return design_data 