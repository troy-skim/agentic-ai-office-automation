from app.utils.pdf_utils import ingest_pdf
from app.utils.doc_type_detector import get_doc_type
from app.extractors.application_form import extract_application_fields
from app.routers.gsheet_writer import write_to_gsheet


def run_application_form_pipeline(pdf_path: str, spreadsheet_name: str = "Application"):
    """Pipeline for processing application forms.

    Args:
        pdf_path (str): File path
        spreadsheet_name (str, optional): Name of the Google Spreadsheet. Defaults to "Application".
    """
    # Ingest PDF
    staged_path = ingest_pdf(pdf_path)

    # Extract fields
    extracted_data = extract_application_fields(staged_path)

    # Write to Google Sheet
    write_to_gsheet(extracted_data, "Sheet1", "Application")

    print(
        f"✅ Application form pipeline complete. Data written to Google Sheet: {spreadsheet_name}"
    )
