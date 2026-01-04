import os
import hashlib
import pandas as pd
from extract_text import extract_text_from_pdf
from extract_tables import extract_tables_from_pdf
from ocr_fallback import ocr_pdf
from classify_pdf import classify_document
from extract_facts import extract_facts, save_facts
from router import route_facts
from gemini_vision import analyze_low_quality_text

RAW_DIR = "data/raw"

def run():
    if not os.path.exists(RAW_DIR):
        print(f"❌ {RAW_DIR} does not exist!")
        return
    
    for task in os.listdir(RAW_DIR):
        task_dir = os.path.join(RAW_DIR, task)
        
        if not os.path.isdir(task_dir):
            continue

        print(f"\n📂 Processing task: {task}")

        for pdf_file in os.listdir(task_dir):
            if not pdf_file.endswith('.pdf'):
                continue
                
            pdf_path = os.path.join(task_dir, pdf_file)
            pdf_id = hashlib.md5(pdf_file.encode()).hexdigest()

            print(f"📄 {pdf_file}")

            try:
                # Step 1: Try text extraction
                text, ok = extract_text_from_pdf(pdf_path)

                # Step 2: OCR fallback if needed
                if not ok:
                    print("  ⚠️  Low quality text, applying OCR...")
                    text = ocr_pdf(pdf_path, pdf_id)
                    vision = analyze_low_quality_text(text, task)
                else:
                    vision = None

                # Step 3: Classify document
                classification = classify_document(text, task)
                print(f"  📋 Classification: {classification['confidence']} confidence")

                # Step 4: Extract tables
                tables = extract_tables_from_pdf(pdf_path)
                print(f"  📊 Found {len(tables)} tables")

                # Step 5: Extract facts
                if tables:
                    facts = extract_facts(
                        tables,
                        classification,
                        {"pdf": pdf_file, "task": task}
                    )

                    # Step 6: Save and route facts
                    save_facts(facts, pdf_id)
                    route_facts(facts)
                else:
                    print("  ⚠️  No tables found")

            except Exception as e:
                print(f"  ❌ Error processing {pdf_file}: {e}")
                continue

    print("\n✅ Extraction pipeline complete")

if __name__ == "__main__":
    run()