class RelationshipManager:
    def __init__(self):
        self.protocol_options = [
            "HTTP",
            "gRPC",
            "WebSocket",
            "Query",
            "Other"
        ]

    def infer_relationships_from_workflows(self, design_data):
        """Infer relationships from workflow steps."""
        inferred_relationships = []
        for workflow in design_data.get("workflows", []):
            steps = workflow["steps"]
            for i in range(len(steps) - 1):
                source = steps[i]["step"].strip()
                target = steps[i + 1]["step"].strip()
                # Only add if not already in the list
                rel = f"{source} -> {target}"
                if not any(r["relationship"] == rel for r in inferred_relationships):
                    # Only set description if source is a Client component
                    description = workflow["api"] if i == 0 else ""
                    inferred_relationships.append({
                        "relationship": rel,
                        "description": description,
                        "protocol": "HTTP"  # Default protocol
                    })
        return inferred_relationships

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