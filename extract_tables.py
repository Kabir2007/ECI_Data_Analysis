import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    tables = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted_tables = page.extract_tables()
                
                if not extracted_tables:
                    continue
                    
                for table in extracted_tables:
                    if table and len(table) > 1:
                        try:
                            df = pd.DataFrame(table[1:], columns=table[0])
                            tables.append(df)
                        except Exception as e:
                            print(f"⚠️  Table conversion error: {e}")
                            continue
    except Exception as e:
        print(f"❌ PDF table extraction error: {e}")
    
    return tables