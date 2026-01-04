import json
import os

def extract_facts(tables, classification, meta):
    facts = []

    for df in tables:
        for _, row in df.iterrows():
            facts.append({
                "category": classification.get("data_categories", []),
                "geo_level": classification.get("geographic_level", "unclear"),
                "values": row.to_dict(),
                "source": meta,
                "confidence": classification.get("confidence", "low")
            })

    return facts


def save_facts(facts, pdf_id):
    # Create directory if it doesn't exist
    facts_dir = "data/extracted/facts"
    os.makedirs(facts_dir, exist_ok=True)
    
    path = os.path.join(facts_dir, f"{pdf_id}.json")
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(facts, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(facts)} facts to {path}")