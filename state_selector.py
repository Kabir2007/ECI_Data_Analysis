# state_selector.py

from collections import defaultdict
import math

REQUIRED_CATEGORIES = {
    "district_population",
    "district_voters",
    "gender_ratio",
    "per_capita_income",
    "age_distribution",
    "migration_data",
    "sir_coverage"
}


def select_best_state(facts):
    by_state = defaultdict(list)

    for f in facts:
        by_state[f["state"]].append(f)

    scores = {}

    for state, entries in by_state.items():
        categories_present = {e["category"] for e in entries}
        coverage = len(categories_present & REQUIRED_CATEGORIES) / len(REQUIRED_CATEGORIES)

        avg_conf = sum(e["confidence"] for e in entries) / len(entries)
        volume = math.log(1 + len(entries))

        scores[state] = {
            "coverage": coverage,
            "confidence": avg_conf,
            "volume": volume
        }

    # Stage 1: max coverage
    max_coverage = max(s["coverage"] for s in scores.values())
    candidates = {k: v for k, v in scores.items() if v["coverage"] == max_coverage}

    # Stage 2: max confidence
    max_conf = max(v["confidence"] for v in candidates.values())
    candidates = {k: v for k, v in candidates.items() if v["confidence"] == max_conf}

    # Stage 3: max volume
    selected = max(candidates.items(), key=lambda x: x[1]["volume"])

    return selected[0], scores


if __name__ == "__main__":
    from usable_facts import extract_usable_facts
    facts = extract_usable_facts()
    state, scores = select_best_state(facts)
    print("Selected State:", state)
    print(scores[state])
