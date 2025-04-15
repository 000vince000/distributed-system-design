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
            else:  # Other type
                diagram.append(f"    {comp}[{comp}]")
        
        # Add relationships
        for rel in design_data["architecture"]["relationships"]:
            source, target = rel["relationship"].split("->")
            source = source.strip()
            target = target.strip()
            protocol = rel["protocol"]
            description = rel["description"]
            
            # Quote the description text
            label = f'"{protocol}: {description}"'
            
            if protocol == "HTTP":
                diagram.append(f"    {source} -->|{label}| {target}")
            elif protocol == "gRPC":
                diagram.append(f"    {source} -.->|{label}| {target}")
            elif protocol == "WebSocket":
                diagram.append(f"    {source} ===|{label}| {target}")
            else:  # Other protocol
                diagram.append(f"    {source} -->|{label}| {target}")
        
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
                # Extract component name from step
                step = steps[i]["step"].strip().lower()
                components.add(step)
                
                # If there's a next step, create a relationship
                if i < len(steps) - 1:
                    next_step = steps[i + 1]["step"].strip().lower()
                    relationships.add((step, next_step))
        
        if not components:
            self.console.print("[yellow]No components found in workflows. Please define workflows first.[/yellow]")
            return design_data
            
        # Get component types
        self.console.print("\n[bold]Specify component types:[/bold]")
        component_types = {}
        for comp in sorted(components):
            self.console.print(f"\nSelect type for {comp}:")
            self.console.print("1. API")
            self.console.print("2. Service")
            self.console.print("3. Database")
            self.console.print("4. Cache")
            self.console.print("5. Other")
            
            type_choice = self.prompt.ask(
                "Select type",
                choices=["1", "2", "3", "4", "5"]
            )
            
            # Map choice to type
            type_map = {
                "1": "API",
                "2": "Service",
                "3": "Database",
                "4": "Cache",
                "5": "Other"
            }
            component_types[comp] = type_map[type_choice]
        
        # Get relationship descriptions and protocols
        self.console.print("\n[bold]Specify relationship details:[/bold]")
        described_relationships = []
        for i, (source, target) in enumerate(sorted(relationships), 1):
            self.console.print(f"\n{i}. {source} -> {target}")
            description = self._get_multi_line_input(
                "Enter relationship description (x to finish):",
                "x"
            )[0]
            
            self.console.print("\nSelect protocol:")
            self.console.print("1. HTTP")
            self.console.print("2. gRPC")
            self.console.print("3. WebSocket")
            self.console.print("4. Other")
            
            protocol_choice = self.prompt.ask(
                "Select protocol",
                choices=["1", "2", "3", "4"]
            )
            
            # Map choice to protocol
            protocol_map = {
                "1": "HTTP",
                "2": "gRPC",
                "3": "WebSocket",
                "4": "Other"
            }
            protocol = protocol_map[protocol_choice]
            
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
                "Enter database tables (TableName: field1:type, field2:type, ...) (x to finish):",
                "x"
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