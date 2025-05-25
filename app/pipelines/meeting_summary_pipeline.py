from app.utils.pdf_utils import ingest_pdf
from app.utils.doc_type_detector import get_doc_type
from app.extractors.meeting_summary import extract_meeting_fields
from app.routers.gsheet_writer import write_to_gsheet
import pandas as pd


def flatten_meeting_dict(data: dict, expand_fields: list[str]) -> list[dict]:
    """Convert a single meeting dict with list fields into a list of flat rows.
    Repeats static metadata fields for each row.

    Args:
        data (dict): Meeting metadata dictionary
        expand_fields (list[str]): The columns set to be expanded

    Returns:
        list[dict]: Lists of dictionaries, each dictionary represents a row
    """
    for field in expand_fields:
        if not isinstance(data.get(field), list):
            data[field] = [data.get(field, "")]

    max_len = max(len(data[field]) for field in expand_fields)

    rows = []
    for i in range(max_len):
        row = {}
        for k, v in data.items():
            if k in expand_fields:
                row[k] = v[i] if i < len(v) else ""
            else:
                row[k] = v  # repeat metadata fields
        rows.append(row)
    return rows


def run_meeting_summary_pipeline(
    pdf_path: str, spreadsheet_name: str = "Meeting_Summary"
):
    """Pipeline for processing meeting reports

    Args:
        pdf_path (str): File path
        spreadsheet_name (str, optional): Name of the Google Sheets document. Defaults to "Meeting_Summary".
    """
    # Ingest PDF
    staged_path = ingest_pdf(pdf_path)

    # Extract structured summary
    summary_data = extract_meeting_fields(staged_path)

    # Flatten data
    exploded_data = flatten_meeting_dict(
        summary_data, expand_fields=["attendees", "agenda", "action_items"]
    )

    # Write to Google Sheet
    write_to_gsheet(exploded_data, "Sheet1", spreadsheet_name)

    print(
        f"✅ Meeting summary pipeline complete. Data written to Google Sheet: {spreadsheet_name}"
    )
