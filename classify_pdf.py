import json
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

def classify_document(text, task):
    prompt = f"""
Classify the following document.

TASK:
{task}

Return STRICT JSON:
{{
  "data_categories": ["population", "demographics", "voters", "migration", "admin_process", "none"],
  "geographic_level": "district/state/national/unclear",
  "extraction_mode": "tables/text/both/ignore",
  "confidence": "high/medium/low"
}}

DOCUMENT:
{text[:10000]}
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
        print(f"Classification error: {e}")
        return {
            "data_categories": ["none"],
            "geographic_level": "unclear",
            "extraction_mode": "ignore",
            "confidence": "low"
        }