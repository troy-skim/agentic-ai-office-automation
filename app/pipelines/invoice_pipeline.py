from app.utils.pdf_utils import ingest_pdf
from app.utils.doc_type_detector import get_doc_type
from app.extractors.invoice import extract_invoice_fields
from app.routers.excel_writer import write_to_excel


def run_invoice_pipeline(
    pdf_path: str, output_path: str = "data/sample_outputs/invoice_output.xlsx"
):
    """Pipeline for processing invoices.

    Args:
        pdf_path (str): File path
        output_path (str, optional): File path where the resulting file will be stored. Defaults to "data/sample_outputs/invoice_output.xlsx".
    """
    # Ingest PDF
    staged_path = ingest_pdf(pdf_path)

    # Extract fields
    extracted_data = extract_invoice_fields(staged_path)

    # Write to Excel
    write_to_excel(extracted_data, output_path)

    print(f"✅ Invoice pipeline complete. Output saved to {output_path}")
