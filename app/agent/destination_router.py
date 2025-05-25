import yaml
import os

ROUTING_PATH = os.path.join(
    os.path.dirname(__file__), "../../config/routing_rules.yaml"
)


def load_routing_rules():
    """Load routing rules from YAML file.

    Returns:
        Any: Routing rules
    """
    with open(ROUTING_PATH, "r") as file:
        return yaml.safe_load(file)


def get_destination_for_doc_type(doc_type: str) -> str:
    """Return destination type (e.g., 'excel', 'gsheet', 'airtable') for a given doc_type.

    Args:
        doc_type (str): Document type

    Raises:
        ValueError: No routing rule found

    Returns:
        str: Destination (Excel, Google Sheets)
    """
    rules = load_routing_rules()
    destination = rules.get(doc_type, {}).get("destination")
    if destination is None:
        raise ValueError(f"No routing rule found for document type: '{doc_type}'")
    return destination
