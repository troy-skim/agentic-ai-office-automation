import argparse
from app.pipelines.invoice_pipeline import run_invoice_pipeline
from app.pipelines.application_form_pipeline import run_application_form_pipeline
from app.pipelines.meeting_summary_pipeline import run_meeting_summary_pipeline
from app.utils.doc_type_detector import get_doc_type
from dotenv import load_dotenv

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Agentic AI Office Automation")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("--excel_path", help="Excel file path")
    parser.add_argument("--sheet_name", help="Google Sheet Name for GSheet outputs")
    args = parser.parse_args()

    pdf_path = args.pdf_path
    doc_type = get_doc_type(pdf_path)

    if doc_type == "invoice":
        if not args.excel_path:
            run_invoice_pipeline(pdf_path)
        else:
            run_invoice_pipeline(pdf_path, args.excel_path)
    elif doc_type == "application_form":
        if not args.sheet_name:
            raise ValueError("Google Sheet Name required for application form.")
        run_application_form_pipeline(pdf_path, args.sheet_name)
    elif doc_type == "meeting_summary":
        if not args.sheet_name:
            raise ValueError("Google Sheet Name required for meeting summary.")
        run_meeting_summary_pipeline(pdf_path, args.sheet_name)
    else:
        raise ValueError(f"Unsupported document type: {doc_type}")


if __name__ == "__main__":
    main()
