import json
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

def analyze_low_quality_text(text, task):
    prompt = f"""
You are assisting in extracting numerical data from a
government PDF that was poorly scanned.

TASK:
{task}

Rules:
- Only report numbers explicitly visible
- Do NOT guess missing values
- If unclear, say unclear

Return STRICT JSON:
{{
  "contains_numeric_data": true,
  "data_categories": ["list", "of", "categories"],
  "confidence": "high/medium/low",
  "notes": "brief explanation"
}}

TEXT:
{text[:8000]}
"""
    
    try:
        resp = model.generate_content(prompt)
        text_response = resp.text.strip()
        
        # Remove markdown code blocks if present
        if text_response.startswith("```json"):
            text_response = text_response[7:]
        if text_response.startswith("```"):
            text_response = text_response[3:]
        if text_response.endswith("```"):
            text_response = text_response[:-3]
        text_response = text_response.strip()
        
        return json.loads(text_response)
    except Exception as e:
        print(f"Vision analysis error: {e}")
        return {
            "contains_numeric_data": False,
            "data_categories": [],
            "confidence": "low",
            "notes": "Analysis failed"
        }