import yaml
import os
import re

from app.utils.llm_utils import classify_doc_type_via_llm

with open(os.path.join("config", "doc_types.yaml"), "r") as f:
    DOC_TYPE_KEYWORDS = yaml.safe_load(f)

FALLBACK_CONFIDENCE_THRESHOLD = 0.6


def get_doc_type(text: str) -> str:
    """
    Determine document type using LLM first, then keyword fallback.

    Args:
        text (str): Raw text extracted from a PDF

    Returns:
        str: One of ['invoice', 'application_form', 'meeting_summary', 'resume']
    """
    # Preprocess
    first_lines = "\n".join(text.strip().splitlines()[:15])

    # Try LLM-based classification
    try:
        llm_result = classify_doc_type_via_llm(first_lines)
        doc_type, confidence = llm_result.get("type"), llm_result.get("confidence", 0)

        if (
            doc_type in DOC_TYPE_KEYWORDS
            and confidence >= FALLBACK_CONFIDENCE_THRESHOLD
        ):
            return doc_type

    except Exception as e:
        print(f"⚠️ LLM classification failed: {e}")

    fallback_type = classify_via_keywords(first_lines)
    return fallback_type


def classify_via_keywords(text: str) -> str:
    """
    Simple keyword matching fallback.

    Args:
        text (str): Short sample of document text

    Returns:
        str: Detected doc type
    """
    text_lower = text.lower()
    scores = {}

    for doc_type, keywords in DOC_TYPE_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword.lower() in text_lower)
        scores[doc_type] = score

    return max(scores, key=scores.get)
