class RelationshipManager:
    def __init__(self):
        self.protocol_options = [
            "HTTP",
            "gRPC",
            "WebSocket",
            "Query",
            "Other"
        ]

    def parse_step(self, step_text):
        """Parse a workflow step in 'ComponentA -> ComponentB: action' format.

        Returns (source, target, action), or None if it doesn't match.
        """
        if "->" not in step_text:
            return None
        source, rest = step_text.split("->", 1)
        target, action = rest.split(":", 1) if ":" in rest else (rest, "")
        return source.strip(), target.strip(), action.strip()

    def extract_relationships_from_workflows(self, design_data):
        """Extract relationships from workflow steps already in 'A -> B: action' format."""
        extracted_relationships = []
        for workflow in design_data.get("workflows", []):
            for step in workflow["steps"]:
                parsed = self.parse_step(step["step"])
                if not parsed:
                    continue
                source, target, action = parsed
                rel = f"{source} -> {target}"
                # Only add if not already in the list
                if not any(r["relationship"] == rel for r in extracted_relationships):
                    extracted_relationships.append({
                        "relationship": rel,
                        "description": action,
                        "protocol": "HTTP"  # Default protocol
                    })
        return extracted_relationships

    def format_relationship(self, source, target, description, protocol):
        """Format a relationship with its details."""
        return {
            "relationship": f"{source} -> {target}",
            "description": description,
            "protocol": protocol
        }

    def get_protocol_options(self):
        """Get available protocol options."""
        return self.protocol_options 