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
        
        # Extract components from workflows
        components = set()
        for workflow in design_data.get("workflows", []):
            for step in workflow["steps"]:
                components.add(step["step"].strip().lower())
        
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
        components_list = sorted(components)
        
        while True:
            # Show available components
            self.console.print("\n[bold]Available components:[/bold]")
            for i, comp in enumerate(components_list, 1):
                self.console.print(f"{i}. {comp} ({component_types[comp]})")
            self.console.print("x. Done defining relationships")
            
            # Get relationship in format "source->target"
            self.console.print("\nEnter relationship in format 'source->target' (e.g., '1->3')")
            relationship = self.prompt.ask(
                "Select relationship (or 'x' to finish)"
            )
            
            if relationship.lower() == 'x':
                break
                
            try:
                source_idx, target_idx = relationship.split('->')
                source_idx = int(source_idx.strip())
                target_idx = int(target_idx.strip())
                
                if not (1 <= source_idx <= len(components_list) and 1 <= target_idx <= len(components_list)):
                    self.console.print("[red]Invalid component numbers. Please use numbers from the list above.[/red]")
                    continue
                    
                source = components_list[source_idx - 1]
                target = components_list[target_idx - 1]
            except (ValueError, IndexError):
                self.console.print("[red]Invalid format. Please use 'source->target' (e.g., '1->3')[/red]")
                continue
            
            # Get relationship details
            self.console.print(f"\n[bold]Relationship: {source} -> {target}[/bold]")
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
            
            # Show current relationships
            if described_relationships:
                self.console.print("\n[bold]Current Relationships:[/bold]")
                for rel in described_relationships:
                    self.console.print(f"- {rel['relationship']}")
                    self.console.print(f"  Description: {rel['description']}")
                    self.console.print(f"  Protocol: {rel['protocol']}")
        
        # Get database schema for each Database and Cache component
        schema = []
        storage_components = {comp: type_ for comp, type_ in component_types.items() 
                            if type_ in ["Database", "Cache"]}
        
        if storage_components:
            self.console.print("\n[bold]Enter database schema for each storage component:[/bold]")
            for comp, type_ in storage_components.items():
                self.console.print(f"\n[bold]{type_} Schema for {comp}:[/bold]")
                self.console.print("Enter tables (TableName: field1:type, field2:type, ...)")
                self.console.print("Example: Users: id:int, username:string, email:string")
                self.console.print("Enter 'x' when done with this component")
                
                component_schema = self._get_multi_line_input(
                    f"Enter schema for {comp} (x to finish):",
                    "x"
                )
                if component_schema:
                    schema.extend([f"{comp}: {table}" for table in component_schema])
        
        # Store architecture design
        design_data["architecture"] = {
            "component_types": component_types,
            "relationships": described_relationships,
            "database_schema": schema
        }
        
        # Generate and display Mermaid diagram
        mermaid_diagram = self._generate_mermaid_diagram(design_data)
        self.console.print("\n[bold]Generated Architecture Diagram:[/bold]")
        self.console.print("```mermaid")
        self.console.print(mermaid_diagram)
        self.console.print("```")
        self.console.print("\n[blue]View or edit this diagram at: https://mermaidchart.com[/blue]")
        
        return design_data 