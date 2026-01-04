import json
import os

def route_facts(facts):
    """
    Routes extracted facts to appropriate output files
    based on their category and geographic level.
    """
    
    output_dir = "data/extracted/routed"
    os.makedirs(output_dir, exist_ok=True)
    
    for fact in facts:
        category = fact.get("category", ["unknown"])[0] if isinstance(fact.get("category"), list) else "unknown"
        geo_level = fact.get("geo_level", "unclear")
        
        # Create filename based on category and geo level
        filename = f"{category}_{geo_level}.jsonl"
        filepath = os.path.join(output_dir, filename)
        
        # Append to JSONL file (one JSON object per line)
        with open(filepath, "a", encoding="utf-8") as f:
            json.dump(fact, f, ensure_ascii=False)
            f.write("\n")
    
    print(f"📊 Routed {len(facts)} facts")