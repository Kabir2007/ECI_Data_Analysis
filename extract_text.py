import pdfplumber

def extract_text_from_pdf(pdf_path):
    """
    Returns extracted text and a flag indicating
    whether text extraction was successful.
    """
    full_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text()
            if txt:
                full_text.append(txt)

    text = "\n".join(full_text)
    success = len(text.strip()) > 300  # heuristic

    return text, success
