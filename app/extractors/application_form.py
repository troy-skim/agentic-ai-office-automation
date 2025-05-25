import os
import json
import dotenv
import pymupdf
import google.generativeai as genai
from app.utils.pdf_utils import extract_text_non_form, extract_prompt_from_scanned_form

dotenv.load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def extract_application_fields(pdf_path: str) -> dict:
    """Extract form field values and layout context, sends to Gemini 1.5 Flash for intelligent parsing.
    Return a dictionary of semantic field names and user-provided values.

    Args:
        pdf_path (str): Path to the file

    Returns:
        dict: Dictionary of semantic field names and user-provided values
    """
    # Extract layout text for context
    print("[INFO] Extracting layout text for prompt context...")
    layout_text = extract_text_non_form(pdf_path)
    layout_lines = layout_text.splitlines()
    layout_lines = [line for line in layout_lines if len(line.strip()) < 100]
    layout_text = "\n".join(layout_lines)

    # Extract raw form field values
    print("[INFO] Extracting raw field values from PDF widgets...")
    doc = pymupdf.open(pdf_path)
    raw_fields = {}
    for page in doc:
        widgets = page.widgets()
        if not widgets:
            continue
        for widget in widgets:
            key = widget.field_name
            value = widget.field_value

            # Handle checkboxes (Yes / No)
            if key:
                val_clean = str(value).strip().lower() if value is not None else ""
                if val_clean in ["yes", "on", "true", "1"]:
                    raw_fields[key] = "Yes"
                elif val_clean in ["off", "no", "", "none"]:
                    raw_fields[key] = "No"
                else:
                    raw_fields[key] = value

    # Construct LLM prompt
    if not raw_fields:
        print("[WARN] No form fields found. OCR-only extraction.")
        prompt = extract_prompt_from_scanned_form(pdf_path)
    else:
        prompt = f"""
Given layout text and filled field values from an employment application PDF, extract all extracted data as flat key-value pairs using the following rules: 
- Layout may contain user input (from OCR). Field values use raw IDs (e.g., Text_1)
- Keys must be in lowercase snake_case
- No spaces, camelCase, markdown, explanation
- Use numbered suffixes for repeated fields (e.g., education_1, employment_2)
- No nested objects or arrays
- Respond with only a valid Python dictionary mapping semantic field names to values

Example:
{{"first_name": "John", "email": "john@example.com"}}

Layout:
{layout_text}

Fields:
{raw_fields}
""".strip()

    # Call Gemini
    print("[INFO] Sending to Gemini 1.5 Flash...")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    raw_output = response.text.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.strip("```").strip()
        if raw_output.startswith("python"):
            raw_output = raw_output[len("python") :].strip()

    try:
        extracted = json.loads(raw_output)
        if not isinstance(extracted, dict):
            raise ValueError("Parsed response is not a dictionary.")
        print("[INFO] Gemini extraction successful.")
        return extracted

    except Exception as e:
        print(f"[ERROR] Failed to parse Gemini output: {e}")
        print("[RAW OUTPUT]:", response.text)
        return {}
