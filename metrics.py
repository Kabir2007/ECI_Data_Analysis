# metrics.py

from collections import defaultdict
import statistics


def compute_metrics(facts, selected_state):
    by_district = defaultdict(list)

    for f in facts:
        if f["state"] == selected_state and f["district"]:
            by_district[f["district"]].append(f)

    district_scores = {}

    for district, entries in by_district.items():
        pop = voters = gender = sir = mig = None

        for e in entries:
            if e["category"] == "district_population":
                pop = e["value"]
            elif e["category"] == "district_voters":
                voters = e["value"]
            elif e["category"] == "gender_ratio":
                gender = e["value"]
            elif e["category"] == "sir_coverage":
                sir = e["value"]
            elif e["category"] == "migration_data":
                mig = e["value"]

        # --- Health ---
        health_components = []

        if pop and voters:
            ratio = voters / pop
            ratio = min(max(ratio, 0.8), 1.0)
            health_components.append(ratio)

        if gender:
            health_components.append(1 - abs(gender - 950) / 300)

        if sir:
            health_components.append(sir)

        health_score = statistics.mean(health_components) if health_components else None

        # --- Migration ---
        migration_score = (mig / pop) if mig and pop else None

        district_scores[district] = {
            "health_score": health_score,
            "migration_pressure": migration_score
        }

    # State aggregate
    valid_health = [v["health_score"] for v in district_scores.values() if v["health_score"] is not None]
    valid_migration = [v["migration_pressure"] for v in district_scores.values() if v["migration_pressure"] is not None]

    state_metrics = {
        "state_health": statistics.mean(valid_health) if valid_health else None,
        "state_migration_pressure": statistics.mean(valid_migration) if valid_migration else None
    }

    return district_scores, state_metrics


if __name__ == "__main__":
    from usable_facts import extract_usable_facts
    from state_selector import select_best_state

    facts = extract_usable_facts()
    state, _ = select_best_state(facts)
    d, s = compute_metrics(facts, state)

    print("STATE:", state)
    print("STATE METRICS:", s)
