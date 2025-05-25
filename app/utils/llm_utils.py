import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (assumes .env is at project root)
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# System prompt to keep responses predictable
SYSTEM_PROMPT = """
Classify this document. Reply only in this format:
type: <invoice | application_form | meeting_summary | resume>
confidence: <0.0 - 1.0>
"""


def classify_doc_type_via_llm(text_sample: str) -> dict:
    """
    Use Gemini to classify the document type based on text.

    Args:
        text_sample (str): The first ~10–15 lines of text from a PDF.

    Returns:
        dict: {"type": <doc_type>, "confidence": <float>}
    """
    prompt = f"{SYSTEM_PROMPT}\n\n---\n{text_sample.strip()}\n---"

    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        response = model.generate_content(prompt)
        output = response.text.strip()

        # Parse the structured response
        doc_type, confidence = None, 0.0
        for line in output.splitlines():
            if line.lower().startswith("type:"):
                doc_type = line.split(":", 1)[1].strip()
            elif line.lower().startswith("confidence:"):
                confidence = float(line.split(":", 1)[1].strip())

        return {"type": doc_type, "confidence": confidence}

    except Exception as e:
        print(f"LLM error: {e}")
        return {"type": None, "confidence": 0.0}
