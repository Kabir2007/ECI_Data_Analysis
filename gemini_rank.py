# gemini_rank.py
'''
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_MAX_CHARS

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(GEMINI_MODEL)


def truncate_text(text, max_chars=GEMINI_MAX_CHARS):
    """
    Prevents sending excessively large PDFs to Gemini.
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars]


def gemini_score_document(
    document_text: str,
    task_description: str,
    required_keywords: list,
    preferred_level: str
):
    """
    Uses Gemini to evaluate how well a document matches a task.

    Returns:
    {
        "score": float (0-1),
        "explanation": str,
        "detected_level": str
    }
    """

    truncated_text = truncate_text(document_text)

    prompt = f"""
You are assisting an election research project.
You are NOT modifying electoral rolls or voter data.

TASK:
{task_description}

PREFERRED DATA LEVEL:
{preferred_level}

REQUIRED KEYWORDS:
{", ".join(required_keywords)}

INSTRUCTIONS:
1. Analyze the document text.
2. Decide how relevant it is for the task.
3. Score relevance from 0 to 1.
4. Explain the reasoning in simple, factual language.
5. Identify the data granularity (national / state / district / constituency / unclear).
6. If data is anecdotal, incomplete, or media-based, penalize score.

OUTPUT FORMAT (STRICT JSON):
{{
  "score": number,
  "explanation": string,
  "detected_level": string
}}

DOCUMENT TEXT:
\"\"\"
{truncated_text}
\"\"\"
"""

    response = model.generate_content(prompt)

    try:
        text = response.text.strip()
        return eval(text)  # Controlled eval: Gemini outputs strict JSON
    except Exception:
        return {
            "score": 0.0,
            "explanation": "Gemini could not confidently assess this document.",
            "detected_level": "unknown"
        } '''

# gemini_rank.py

import json
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_MAX_CHARS

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(GEMINI_MODEL)


def truncate_text(text, max_chars=GEMINI_MAX_CHARS):
    """
    Prevents sending excessively large PDFs to Gemini.
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars]


def gemini_score_document(
    document_text: str,
    task_description: str,
    required_keywords: list,
    preferred_level: str
):
    """
    Uses Gemini to evaluate how well a document matches a task.

    Returns:
    {
        "score": float (0-1),
        "explanation": str,
        "detected_level": str
    }
    """

    truncated_text = truncate_text(document_text)

    prompt = f"""
You are assisting an election research project.
You are NOT modifying electoral rolls or voter data.

TASK:
{task_description}

PREFERRED DATA LEVEL:
{preferred_level}

REQUIRED KEYWORDS:
{", ".join(required_keywords)}

INSTRUCTIONS:
1. Analyze the document text.
2. Decide how relevant it is for the task.
3. Score relevance from 0 to 1.
4. Explain the reasoning in simple, factual language.
5. Identify the data granularity (national / state / district / constituency / unclear).
6. If data is anecdotal, incomplete, or media-based, penalize score.

OUTPUT FORMAT (STRICT JSON):
{{
  "score": number,
  "explanation": string,
  "detected_level": string
}}

DOCUMENT TEXT:
\"\"\"
{truncated_text}
\"\"\"
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        
        # Use json.loads instead of eval for security
        result = json.loads(text)
        
        # Validate the response structure
        if not all(k in result for k in ["score", "explanation", "detected_level"]):
            raise ValueError("Missing required keys in response")
            
        return result
        
    except Exception as e:
        print(f"Gemini parsing error: {e}")
        return {
            "score": 0.0,
            "explanation": "Gemini could not confidently assess this document.",
            "detected_level": "unknown"
        }
