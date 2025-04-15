from .base_step import BaseStep

class ArchitectureStep(BaseStep):
    def _generate_mermaid_diagram(self, design_data):
        """Generate a Mermaid diagram from the architecture design."""
        diagram = ["graph TD"]
        
        # Add components with their types
        for comp, type_ in design_data["architecture"]["component_types"].items():
            if type_ == "API":
                diagram.append(f"    {comp}[{comp}]")
            elif type_ == "Service":
                diagram.append(f"    {comp}(({comp}))")
            elif type_ == "Database":
                diagram.append(f"    {comp}[(Database)]")
            elif type_ == "Cache":
                diagram.append(f"    {comp}[(Cache)]")
        
        # Add relationships
        for rel in design_data["architecture"]["relationships"]:
            source, target = rel["relationship"].split("->")
            source = source.strip()
            target = target.strip()
            protocol = rel["protocol"]
            description = rel["description"]
            
            if protocol == "HTTP":
                diagram.append(f"    {source} -->|HTTP: {description}| {target}")
            elif protocol == "gRPC":
                diagram.append(f"    {source} -.->|gRPC: {description}| {target}")
            elif protocol == "WebSocket":
                diagram.append(f"    {source} ===|WS: {description}| {target}")
            elif protocol == "Database":
                diagram.append(f"    {source} --|DB: {description}| {target}")
        
        return "\n".join(diagram)

    def execute(self, design_data):
        """Design system architecture and database schema."""
        self.console.print("\n[bold]Step 4: Architecture Diagramming[/bold]")
        
        # Extract components and relationships from workflows
        components = set()
        relationships = set()
        
        for workflow in design_data.get("workflows", []):
            steps = workflow["steps"]
            for i in range(len(steps)):
                # Extract service names from step descriptions
                step = steps[i]["step"].lower()
                services = ["client", "userservice", "mappingservice", "notificationservice"]
                service = next((s for s in services if s in step), None)
                if service:
                    components.add(service)
                    if i < len(steps) - 1:
                        next_step = steps[i + 1]["step"].lower()
                        next_service = next((s for s in services if s in next_step), None)
                        if next_service:
                            relationships.add((service, next_service))
        
        if not components:
            self.console.print("[yellow]No components found in workflows. Please define workflows first.[/yellow]")
            return design_data
            
        # Get component types
        self.console.print("\n[bold]Specify component types:[/bold]")
        component_types = {}
        for comp in sorted(components):
            type_choice = self.prompt.ask(
                f"Select type for {comp}",
                choices=["API", "Service", "Database", "Cache"]
            )
            component_types[comp] = type_choice
        
        # Get relationship descriptions and protocols
        self.console.print("\n[bold]Specify relationship details:[/bold]")
        described_relationships = []
        for i, (source, target) in enumerate(sorted(relationships), 1):
            self.console.print(f"\n{i}. {source} -> {target}")
            description = self._get_multi_line_input(
                "Enter relationship description (END to finish):",
                "END"
            )[0]
            protocol = self.prompt.ask(
                "Select protocol",
                choices=["HTTP", "gRPC", "WebSocket", "Database"]
            )
            described_relationships.append({
                "relationship": f"{source} -> {target}",
                "description": description,
                "protocol": protocol
            })
        
        # Only ask for database schema if we have Database or Cache components
        schema = []
        if any(t in ["Database", "Cache"] for t in component_types.values()):
            self.console.print("\n[bold]Enter database schema:[/bold]")
            schema = self._get_multi_line_input(
                "Enter database tables (TableName: field1:type, field2:type, ...) (END to finish):",
                "END"
            )
        
        # Store architecture design
        design_data["architecture"] = {
            "component_types": component_types,
            "relationships": described_relationships,
            "database_schema": schema
        }
        
        # Generate and display Mermaid diagram
        mermaid_diagram = self._generate_mermaid_diagram(design_data)
        self.console.print("\n[bold]Architecture Diagram:[/bold]")
        self.console.print("```mermaid")
        self.console.print(mermaid_diagram)
        self.console.print("```")
        
        return design_data 