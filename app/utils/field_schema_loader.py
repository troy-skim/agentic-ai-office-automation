import yaml
import os

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "../../config/field_schemas.yaml")


def load_field_schema():
    with open(SCHEMA_PATH, "r") as f:
        return yaml.safe_load(f)


def normalize_keys(doc_type: str, raw_data: dict) -> dict:
    """Normalize extracted keys using field schema and aliases."""
    schema_data = load_field_schema()
    schema = schema_data.get(doc_type, {})
    aliases = schema_data.get("_aliases", {})

    normalized = {}

    # Reverse alias map for quick lookup
    reverse_alias_map = {}
    for canonical, alias_list in aliases.items():
        for alias in alias_list:
            reverse_alias_map[alias] = canonical

    for key, value in raw_data.items():
        # Direct match
        if key in schema:
            normalized[key] = value
        # Alias match
        elif key in reverse_alias_map:
            canonical_key = reverse_alias_map[key]
            normalized[canonical_key] = value
        else:
            normalized[key] = value

    return normalized
