import os
import dotenv
import ast
import google.generativeai as genai
from app.utils.pdf_utils import extract_text_non_form

dotenv.load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def extract_meeting_fields(pdf_path: str) -> dict:
    """Extract structured fields from a meeting summary PDF using Gemini.

    Args:
        pdf_path (str): File path

    Returns:
        dict: Key-value dataset
    """
    # Extract raw text from PDF
    raw_text = extract_text_non_form(pdf_path)

    # Clean long legal/disclaimer lines
    lines = raw_text.splitlines()
    lines = [line for line in lines if len(line.strip()) < 100]
    raw_text = "\n".join(lines)

    # Compose LLM prompt
    prompt = f"""
Extract key meeting information from the following text.

Output a valid Python dictionary with any of these fields if available:
- title
- date
- time
- location
- attendees
- agenda (list)
- summary (paragraph)
- action_items (list)
- decisions (list)
- next_meeting (str)

Respond with only the dictionary. No markdown, no explanation.

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

        result = ast.literal_eval(cleaned)
        if not isinstance(result, dict):
            raise ValueError("Gemini output is not a dict.")

        print("[INFO] Gemini meeting summary parsed successfully.")
        return result

    except Exception as e:
        print(f"[ERROR] Failed to extract meeting summary: {e}")
        print("[RAW LLM OUTPUT]:", response.text)
        return {}
