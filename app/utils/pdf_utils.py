import os
import re
import dotenv
import shutil
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
import google.generativeai as genai

UPLOAD_DIR = "data/sample_pdfs"
dotenv.load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def ingest_pdf(pdf_path: str) -> str:
    """Validate and copy PDF file to staging upload folder"""
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
    if not pdf_path.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported.")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    dest_path = os.path.join(UPLOAD_DIR, os.path.basename(pdf_path))
    if os.path.abspath(pdf_path) != os.path.abspath(dest_path):
        shutil.copy2(pdf_path, dest_path)
    print(f"PDF successfully ingested: {dest_path}")
    return dest_path


def extract_text_from_text_layout(pdf_path: str) -> str:
    """Extract text from the pdf using pdfplumber"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text.strip()


def extract_text_from_image(pdf_path: str) -> str:
    """Extract text from the pdf using ocr, when pdf is image based"""
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text.strip()


def extract_text_non_form(pdf_path: str) -> str:
    """Wrapper function for choosing between pdfplumber and ocr"""
    text = extract_text_from_text_layout(pdf_path)
    cleaned = re.sub(r"\s+", "", text)

    if not cleaned:
        text = extract_text_from_image(pdf_path)
    return text


def extract_prompt_from_scanned_form(pdf_path: str) -> str:
    """Extract prompt for an image based fields format"""
    ocr_text = extract_text_from_image(pdf_path)

    # Prompt Gemini with layout only (no field values)
    prompt = f"""
         Extract all extracted data as flat key-value pairs using the following rules: 
            - Keys must be in lowercase snake_case
            - No spaces, camelCase, markdown, explanation
            - Use numbered suffixes for repeated fields (e.g., education_1, employment_2)
            - No nested objects or arrays
            - Respond with only a valid Python dictionary

        layout:
        {ocr_text}
    """.strip()

    return prompt
