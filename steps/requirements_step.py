from .base_step import BaseStep

class RequirementsStep(BaseStep):
    def execute(self, design_data):
        """Gather functional and non-functional requirements."""
        self.navigation_helper.display_step_header(1)
        
        self.console.print("\n[bold]Functional Requirements:[/bold]")
        design_data["requirements"]["functional"] = self.input_helper.get_multi_line_input(
            "Enter functional requirements (one per line, empty line to finish):"
        )

        self.console.print("\n[bold]Non-functional Requirements:[/bold]")
        self.console.print(
            "[muted]Tip: scope each to the flow(s) it governs rather than the whole system, "
            "e.g. 'strong consistency for order creation/transfers; eventual consistency for "
            "ticker lookup' — different flows often need different guarantees.[/muted]"
        )
        design_data["requirements"]["nonfunctional"] = self.input_helper.get_multi_line_input(
            "Enter non-functional requirements (one per line, empty line to finish):"
        )

        self.console.print("\n[bold]Out of Scope:[/bold]")
        design_data["requirements"]["out_of_scope"] = self.input_helper.get_multi_line_input(
            "Enter things considered but explicitly discarded, e.g. for lack of time (one per line, empty line to finish):"
        )

        return design_data