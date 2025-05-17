class DiagramGenerator:
    def __init__(self):
        pass

    def generate_mermaid_diagram(self, design_data):
        """Generate a Mermaid diagram from the architecture design."""
        diagram = ["graph TD"]
        
        # Add components with their types
        comp_name_map = {}
        for comp, type_ in design_data["architecture"]["component_types"].items():
            comp_id = comp.replace(" ", "")
            comp_name_map[comp] = comp_id
            if type_ == "API":
                diagram.append(f"    {comp_id}[{comp}]")
            elif type_ == "Service":
                diagram.append(f"    {comp_id}(({comp}))")
            elif type_ == "Database":
                diagram.append(f"    {comp_id}[(Database)]")
            elif type_ == "Cache":
                diagram.append(f"    {comp_id}[(Cache)]")
            else:  # Other type
                diagram.append(f"    {comp_id}[{comp}]")
        
        # Add relationships
        for rel in design_data["architecture"]["relationships"]:
            source, target = rel["relationship"].split("->")
            source = source.strip()
            target = target.strip()
            protocol = rel["protocol"]
            description = rel["description"]
            
            # Quote the description text
            label = f'"{protocol}: {description}"'
            
            source_id = comp_name_map.get(source, source.replace(" ", ""))
            target_id = comp_name_map.get(target, target.replace(" ", ""))
            
            if protocol == "HTTP":
                diagram.append(f"    {source_id} -->|{label}| {target_id}")
            elif protocol == "gRPC":
                diagram.append(f"    {source_id} -.->|{label}| {target_id}")
            elif protocol == "WebSocket":
                diagram.append(f"    {source_id} ===|{label}| {target_id}")
            else:  # Other protocol
                diagram.append(f"    {source_id} -->|{label}| {target_id}")
        
        # Add database and cache schema as subgraphs
        if "database_schema" in design_data["architecture"]:
            from collections import defaultdict
            storage_tables = defaultdict(list)
            for entry in design_data["architecture"]["database_schema"]:
                if ":" in entry:
                    storage, table = entry.split(":", 1)
                    storage = storage.strip()
                    table = table.strip()
                    storage_id = comp_name_map.get(storage, storage.replace(" ", ""))
                    storage_tables[storage_id].append((storage, table))
            for storage_id, table_entries in storage_tables.items():
                storage = table_entries[0][0]
                subgraph_name = f"Schema for {storage}"
                diagram.append(f"    subgraph \"{subgraph_name}\"")
                table_nodes = []
                for idx, (storage_name, table) in enumerate(table_entries):
                    node_name = f"{storage_id}_table{idx}"
                    diagram.append(f"        {node_name}[\"{table}\"]")
                    table_nodes.append(node_name)
                diagram.append(f"    end")
                # Connect storage node (db or cache) to each table node with a solid line
                for node_name in table_nodes:
                    diagram.append(f"    {storage_id} --- {node_name}")
        
        return "\n".join(diagram) 