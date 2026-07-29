from rich.markup import escape
from .base_step import BaseStep
from .diagram_generator import DiagramGenerator
from .relationship_manager import RelationshipManager
from .schema_manager import SchemaManager

class ArchitectureStep(BaseStep):
    def __init__(self, console=None):
        super().__init__(console)
        self.diagram_generator = DiagramGenerator()
        self.relationship_manager = RelationshipManager()
        self.schema_manager = SchemaManager()

    def execute(self, design_data):
        """Design system architecture and database schema."""
        self.navigation_helper.display_step_header(5)
        
        # Check if architecture is already defined
        if "architecture" in design_data and design_data["architecture"]:
            self.console.print("[success]Architecture is already defined. Moving to next step.[/success]")
            return design_data
        
        # Extract components from workflows, tracking which workflow/step each came from
        components = set()
        component_sources = {}  # comp -> list of (workflow_api, step_text)
        for workflow in design_data.get("workflows", []):
            for step in workflow["steps"]:
                parsed = self.relationship_manager.parse_step(step["step"])
                if not parsed:
                    self.console.print(f"[warning]Warning: could not parse step '{step['step']}' as 'A -> B: action' — skipping.[/warning]")
                    continue
                for comp in set((parsed[0], parsed[1])):
                    components.add(comp)
                    component_sources.setdefault(comp, []).append((workflow["api"], step["step"]))

        if not components:
            self.console.print("[warning]No components found in workflows. Please define workflows first.[/warning]")
            return design_data

        # Get component types
        self.console.print("\n[bold]Specify component types:[/bold]")
        component_types = {}
        type_options = [
            "Client",
            "API",
            "Service",
            "Database",
            "Cache",
            "Other"
        ]

        # Auto-detect obvious types from naming conventions, checked in order
        # (most specific first) so e.g. a name matching both "cache" and
        # "service" resolves to Cache rather than Service.
        auto_type_rules = [
            (["db", "database", "postgres", "dynamo"], "Database"),
            (["cache"], "Cache"),
            (["service"], "Service"),
        ]

        for comp in sorted(components):
            comp_lower = comp.lower()
            auto_type = next(
                (type_ for keywords, type_ in auto_type_rules if any(kw in comp_lower for kw in keywords)),
                None
            )
            if auto_type:
                component_types[comp] = auto_type
                self.console.print(f"\n[success]Auto-detected type for {escape(comp)}: {auto_type}[/success]")
                continue

            self.console.print(f"\nSelect type for {escape(comp)}:")
            for workflow_api, step_text in component_sources.get(comp, []):
                self.console.print(f"  [muted]{escape(workflow_api)}: {escape(step_text)}[/muted]")
            self.display_helper.display_list(type_options, enumerate_items=True)
            
            type_choice = self.input_helper.get_choice(
                "Select type",
                choices=[str(i) for i in range(1, len(type_options) + 1)],
                show_choices=False
            )
            component_types[comp] = type_options[int(type_choice) - 1]
        
        # Extract relationships from workflows
        described_relationships = self.relationship_manager.extract_relationships_from_workflows(design_data)
        
        # Fix protocols for database relationships
        for rel in described_relationships:
            target = rel["relationship"].split("->")[1].strip()
            if component_types[target] == "Database":
                rel["protocol"] = "Query"

        # update protocols for service to service relationships
        for rel in described_relationships:
            if component_types[rel["relationship"].split("->")[0].strip()] == "Service" and component_types[rel["relationship"].split("->")[1].strip()] == "Service":
                rel["protocol"] = "gRPC"

        # Get relationship descriptions and protocols
        self.console.print("\n[bold]Specify relationship details:[/bold]")
        components_list = sorted(components)
        
        while True:
            # Show current relationships
            if described_relationships:
                self.console.print("\n[bold]Current Relationships:[/bold]")
                for i, rel in enumerate(described_relationships, 1):
                    self.console.print(f"{i}. {rel['relationship']}")
                    self.console.print(f"   Description: {rel['description']}")
                    self.console.print(f"   Protocol: {rel['protocol']}")
            
            # Show available components
            self.console.print("\n[bold]Available components:[/bold]")
            for i, comp in enumerate(components_list, 1):
                self.console.print(f"{i}. {comp} ({component_types[comp]})")
            
            self.console.print("\n[bold]Relationship Options:[/bold]")
            options = [
                "Add new relationship",
                "Delete relationship",
                "Edit relationship",
            ]
            self.display_helper.display_list(options, enumerate_items=True)
            self.console.print(f"{self.input_helper.SKIP_CHOICE}. Done defining relationships")

            choice = self.input_helper.get_choice(
                "Select option",
                choices=["1", "2", "3", self.input_helper.SKIP_CHOICE],
                show_choices=False
            )
            
            if choice == self.input_helper.SKIP_CHOICE:
                break
            elif choice == "1":  # Add
                # Get relationship in format "source->target"
                self.console.print("\nEnter relationship in format 'source->target' (e.g., '1->3')")
                relationship = self.input_helper.get_choice(
                    "Select relationship",
                    choices=[f"{i}->{j}" for i in range(1, len(components_list) + 1)
                            for j in range(1, len(components_list) + 1) if i != j],
                    show_choices=False
                )
                
                try:
                    source_idx, target_idx = relationship.split('->')
                    source_idx = int(source_idx.strip())
                    target_idx = int(target_idx.strip())
                    
                    if not (1 <= source_idx <= len(components_list) and 1 <= target_idx <= len(components_list)):
                        self.console.print("[error]Invalid component numbers. Please use numbers from the list above.[/error]")
                        continue
                        
                    source = components_list[source_idx - 1]
                    target = components_list[target_idx - 1]
                    
                    # Get relationship details
                    self.console.print(f"\n[bold]Relationship: {source} -> {target}[/bold]")
                    description_lines = self.input_helper.get_multi_line_input(
                        "Enter relationship description (empty line to finish):"
                    )
                    description = description_lines[0] if description_lines else ""
                    
                    protocol_options = self.relationship_manager.get_protocol_options()
                    self.display_helper.display_list(protocol_options, enumerate_items=True)
                
                    protocol_choice = self.input_helper.get_choice(
                        "Select protocol",
                        choices=[str(i) for i in range(1, len(protocol_options) + 1)],
                        show_choices=False
                    )
                
                    described_relationships.append(
                        self.relationship_manager.format_relationship(
                            source, target, description, protocol_options[int(protocol_choice) - 1]
                        )
                    )
                except (ValueError, IndexError):
                    self.console.print("[error]Invalid format. Please use 'source->target' (e.g., '1->3')[/error]")
                    continue
            
            elif choice == "2":  # Delete
                if not described_relationships:
                    self.console.print("[warning]No relationships to delete.[/warning]")
                    continue
                    
                rel_idx = self.input_helper.get_choice(
                    "Enter relationship number to delete",
                    choices=[str(i) for i in range(1, len(described_relationships) + 1)],
                    show_choices=False
                )
                del described_relationships[int(rel_idx) - 1]
                self.console.print("[success]Relationship deleted.[/success]")
                
            elif choice == "3":  # Edit
                if not described_relationships:
                    self.console.print("[warning]No relationships to edit.[/warning]")
                    continue
                    
                rel_idx = self.input_helper.get_choice(
                    "Enter relationship number to edit",
                    choices=[str(i) for i in range(1, len(described_relationships) + 1)],
                    show_choices=False
                )
                rel = described_relationships[int(rel_idx) - 1]
                
                # Edit description
                self.console.print(f"\n[bold]Current description: {rel['description']}[/bold]")
                description_lines = self.input_helper.get_multi_line_input(
                    "Enter new description (empty line to keep current):"
                )
                if description_lines:
                    rel["description"] = description_lines[0]
                
                # Edit protocol
                self.console.print(f"\n[bold]Current protocol: {rel['protocol']}[/bold]")
                protocol_options = self.relationship_manager.get_protocol_options()
                self.display_helper.display_list(protocol_options, enumerate_items=True)
                
                protocol_choice = self.input_helper.get_choice(
                    "Select protocol (x to keep current)",
                    choices=[str(i) for i in range(1, len(protocol_options) + 1)] + [self.input_helper.SKIP_CHOICE],
                    skip_prompt=True,
                    show_choices=False
                )
                
                if protocol_choice != self.input_helper.SKIP_CHOICE:
                    rel["protocol"] = protocol_options[int(protocol_choice) - 1]
        
        # Get database schema for each Database and Cache component
        schema = []
        storage_components = self.schema_manager.get_storage_components(component_types)
        
        if storage_components:
            self.console.print("\n[bold]Enter database schema for each storage component:[/bold]")
            for comp, type_ in storage_components.items():
                self.console.print(f"\n[bold]{type_} Schema for {comp}:[/bold]")
                self.console.print("Enter tables (TableName: field1:type, field2:type, ...)")
                self.console.print("Example: Users: id:int, username:string, email:string")
                self.console.print("Press Enter on a blank line when done with this component")
                
                component_schema = self.input_helper.get_multi_line_input(
                    f"Enter schema for {comp} (empty line to finish):"
                )
                if component_schema:
                    schema.extend([self.schema_manager.format_schema_entry(comp, table) for table in component_schema])
        
        # Store architecture design
        design_data["architecture"] = {
            "component_types": component_types,
            "relationships": described_relationships,
            "database_schema": schema
        }
        
        # Generate and display Mermaid diagram
        mermaid_diagram = self.diagram_generator.generate_mermaid_diagram(design_data)
        self.console.print("\n[bold]Generated Architecture Diagram:[/bold]")
        self.console.print("```mermaid")
        self.console.print(mermaid_diagram)
        self.console.print("```")
        self.console.print("\n[info]View or edit this diagram at: https://mermaidchart.com[/info]")
        
        # Store the mermaid diagram in the architecture data
        design_data["architecture"]["mermaid_diagram"] = mermaid_diagram
        
        return design_data 