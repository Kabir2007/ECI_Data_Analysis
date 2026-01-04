# parse.py

import pdfplumber

def extract_text(pdf_path):
    """
    Extracts text from a PDF file.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text
