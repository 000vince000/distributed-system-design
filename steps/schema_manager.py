class SchemaManager:
    def __init__(self):
        pass

    def get_storage_components(self, component_types):
        """Get storage components (Database and Cache) from component types."""
        return {comp: type_ for comp, type_ in component_types.items() 
                if type_ in ["Database", "Cache"]}

    def format_schema_entry(self, storage, table):
        """Format a schema entry."""
        return f"{storage}: {table}"

    def parse_schema_entry(self, entry):
        """Parse a schema entry into storage and table."""
        if ":" in entry:
            storage, table = entry.split(":", 1)
            return storage.strip(), table.strip()
        return None, None 