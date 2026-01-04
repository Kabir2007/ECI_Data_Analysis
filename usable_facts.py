# usable_facts.py

import json
import re
from pathlib import Path

MIN_CONFIDENCE = 0.6

VALID_CATEGORIES = {
    "district_population",
    "district_voters",
    "gender_ratio",
    "per_capita_income",
    "age_distribution",
    "migration_data",
    "sir_coverage"
}


def is_valid_number(x):
    try:
        x = float(x)
        return not (x != x or x == float("inf"))
    except:
        return False


def clean_numeric(value, category):
    """
    Applies category-specific sanity checks.
    """
    if not is_valid_number(value):
        return None

    value = float(value)

    if category == "gender_ratio":
        if not (600 <= value <= 1200):
            return None

    if category in ["district_population", "district_voters"]:
        if value <= 0 or value > 1e8:
            return None

    if category == "per_capita_income":
        if value < 0 or value > 1e7:
            return None

    return value


def extract_usable_facts(json_dir="data/parsed_json"):
    usable_facts = []

    for path in Path(json_dir).rglob("*.json"):
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                continue

        for entry in data.get("extracted_facts", []):
            category = entry.get("category")
            confidence = entry.get("confidence", 0)

            if category not in VALID_CATEGORIES:
                continue

            if confidence < MIN_CONFIDENCE:
                continue

            value = clean_numeric(entry.get("value"), category)
            if value is None:
                continue

            state = entry.get("state")
            district = entry.get("district")

            if not state:
                continue

            usable_facts.append({
                "state": state,
                "district": district,
                "category": category,
                "value": value,
                "year": entry.get("year"),
                "confidence": confidence,
                "source_file": path.name
            })

    return usable_facts


if __name__ == "__main__":
    facts = extract_usable_facts()
    print(f"Extracted {len(facts)} usable facts.")
