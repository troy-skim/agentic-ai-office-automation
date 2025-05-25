import os
import dotenv
import google.generativeai as genai
from app.utils.pdf_utils import extract_text_non_form

dotenv.load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def extract_invoice_fields(pdf_path: str) -> dict:
    """Extract structured key-value data from an invoice PDF using Gemini.

    Args:
        pdf_path (str): File path

    Returns:
        dict: Key-value dataset
    """
    # Get raw text
    raw_text = extract_text_non_form(pdf_path)

    # Clean up longer lines
    lines = raw_text.splitlines()
    lines = [line for line in lines if len(line.strip()) < 100]
    raw_text = "\n".join(lines)

    # Prompt for LLM
    prompt = f"""
Extract structured key information from this invoice or receipt.

Respond with a valid Python dictionary. Include fields only if they appear.

Preferred keys:
- invoice_number
- date
- due_date
- vendor
- customer
- billing_address
- shipping_address
- line_items: list of {{ description, quantity, unit_price, amount }}
- subtotal
- tax
- discounts
- total
- notes
- payment_info
- terms

Return only a Python dictionary. No explanation or markdown.

text:
{raw_text}
""".strip()

    # Call Gemini
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        cleaned = response.text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("```").strip()
            if cleaned.startswith("python"):
                cleaned = cleaned[len("python") :].strip()

        result = eval(cleaned)
        if not isinstance(result, dict):
            raise ValueError("Gemini output is not a dict.")

        print("[INFO] Gemini invoice parsed successfully.")
        return result

    except Exception as e:
        print(f"[ERROR] Failed to extract invoice: {e}")
        print("[RAW OUTPUT]:", response.text)
        return {}
