from pdf2image import convert_from_path
import pytesseract
import os

def ocr_pdf(pdf_path, pdf_id, out_dir="data/extracted/ocr"):
    os.makedirs(out_dir, exist_ok=True)
    pages = convert_from_path(pdf_path, dpi=300)

    ocr_text = []

    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page, lang="eng")
        page_path = os.path.join(out_dir, f"{pdf_id}_page_{i}.txt")
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(text)

        ocr_text.append(text)

    return "\n".join(ocr_text)
