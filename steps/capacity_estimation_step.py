from .base_step import BaseStep
from .helpers import parse_human_number, format_human_number

class CapacityEstimationStep(BaseStep):
    def execute(self, design_data):
        """Gather back-of-envelope traffic and throughput estimates."""
        self.navigation_helper.display_step_header(2)

        design_data["capacity"] = {"traffic": {}, "throughput": {}}

        self.console.print("\n[bold]a) Traffic:[/bold]")
        users = " ".join(self.input_helper.get_multi_line_input(
            "Active users (e.g. '10M DAU')"
        ))
        read_write_ratio = " ".join(self.input_helper.get_multi_line_input(
            "Read:Write ratio (e.g. '100:1')"
        ))
        avg_qps = " ".join(self.input_helper.get_multi_line_input(
            "Average requests/sec (number, e.g. 500 or 2K)"
        ))
        peak_multiplier = self.input_helper.get_line_input(
            "Peak multiplier over average (e.g. 3)", default="2"
        )

        suggested_peak_qps = ""
        avg_val = parse_human_number(avg_qps)
        mult_val = parse_human_number(peak_multiplier)
        if avg_val is not None and mult_val is not None:
            suggested_peak_qps = format_human_number(avg_val * mult_val)

        peak_qps = self.input_helper.get_line_input(
            "Peak requests/sec"
            + (f" (suggested from avg x multiplier: {suggested_peak_qps})" if suggested_peak_qps else ""),
            default=suggested_peak_qps
        )

        design_data["capacity"]["traffic"] = {
            "users": users,
            "read_write_ratio": read_write_ratio,
            "avg_qps": avg_qps,
            "peak_multiplier": peak_multiplier,
            "peak_qps": peak_qps
        }

        self.console.print("\n[bold]b) Throughput:[/bold]")
        avg_read_payload = " ".join(self.input_helper.get_multi_line_input(
            "Avg read payload/response size (e.g. '2KB')"
        ))
        avg_write_payload = " ".join(self.input_helper.get_multi_line_input(
            "Avg write payload/request size (e.g. '1KB')"
        ))
        bandwidth = " ".join(self.input_helper.get_multi_line_input(
            "Estimated bandwidth (e.g. '50MB/sec peak')"
        ))
        storage_growth = " ".join(self.input_helper.get_multi_line_input(
            "Storage growth (e.g. '500GB/day', or leave blank to skip)"
        ))

        design_data["capacity"]["throughput"] = {
            "avg_read_payload": avg_read_payload,
            "avg_write_payload": avg_write_payload,
            "bandwidth": bandwidth,
            "storage_growth": storage_growth
        }

        return design_data
