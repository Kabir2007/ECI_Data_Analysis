# main.py

from dotenv import load_dotenv
load_dotenv()  # This loads the .env file

import csv
import os
import hashlib

from queries import SEARCH_QUERIES
from search import google_search
from rank import score_result
from download import download_pdf
from parse import extract_text
from gemini_rank import gemini_score_document
from utils import domain_allowed, sha256_file, is_valid_pdf
from config import DRY_RUN, MAX_PDFS_PER_TASK

DATA_INDEX = "data/index.csv"
RAW_DIR = "data/raw"

os.makedirs(RAW_DIR, exist_ok=True)

seen_hashes = set()


def hash_url(url):
    return hashlib.md5(url.encode()).hexdigest()


def compute_penalty(gemini_result, preferred_level):
    penalty = 0.0
    detected = gemini_result.get("detected_level", "unknown")

    if detected == "unclear":
        penalty += 0.2

    if preferred_level == "district" and detected in ["state", "national"]:
        penalty += 0.15

    explanation = gemini_result.get("explanation", "").lower()
    if "news" in explanation or "article" in explanation:
        penalty += 0.3

    return min(penalty, 1.0)


def run():
    from config import GOOGLE_API_KEY, SEARCH_ENGINE_ID
    print(f"API Key: {GOOGLE_API_KEY[:10]}...")
    print(f"Search Engine ID: {SEARCH_ENGINE_ID}")
    
    if not SEARCH_ENGINE_ID:
        print("ERROR: SEARCH_ENGINE_ID is empty!")
        return
    rows = []

    for task in SEARCH_QUERIES:
        print(f"\n🔍 TASK: {task['description']}")

        candidates = []

        # --- SEARCH PHASE ---
        for q in task["queries"]:
            for item in google_search(q):
                det_score = score_result(item, task["required_keywords"])
                candidates.append((det_score, item))

        candidates.sort(key=lambda x: x[0], reverse=True)
        candidates = candidates[:MAX_PDFS_PER_TASK]

        for det_score, item in candidates:
            url = item["link"]

            if not domain_allowed(url):
                continue

            file_id = hash_url(url)
            pdf_path = os.path.join(RAW_DIR, task["id"], f"{file_id}.pdf")

            try:
                if not DRY_RUN:
                    download_pdf(url, f"{file_id}.pdf", task["id"])
                    if not is_valid_pdf(pdf_path):
                        continue

                    pdf_hash = sha256_file(pdf_path)
                    if pdf_hash in seen_hashes:
                        continue

                    seen_hashes.add(pdf_hash)
                    text = extract_text(pdf_path)
                else:
                    text = ""

                # ---- Gemini FAIL-OPEN ----
                if not DRY_RUN and text.strip():
                    gemini_result = gemini_score_document(
                        text,
                        task["description"],
                        task["required_keywords"],
                        task["preferred_level"]
                    )
                else:
                    gemini_result = {
                        "score": 0.0,
                        "explanation": "AI evaluation skipped (dry run or empty document).",
                        "detected_level": "unknown"
                    }

                penalty = compute_penalty(gemini_result, task["preferred_level"])

                final_score = (
                    0.4 * det_score +
                    0.5 * gemini_result["score"] -
                    0.1 * penalty
                )

                rows.append({
                    "task_id": task["id"],
                    "description": task["description"],
                    "url": url,
                    "final_score": round(final_score, 3),

                    # --- Explainability ---
                    "deterministic_score": round(det_score, 3),
                    "gemini_score": round(gemini_result["score"], 3),
                    "penalty": round(penalty, 3),
                    "explanation": gemini_result["explanation"],

                    # --- Legal Metadata ---
                    "detected_data_level": gemini_result["detected_level"],
                    "contains_individual_data": "no",
                    "court_safe": "yes",
                    "used_for_voting_day": "no"
                })

                print(f"✔ {round(final_score,2)} | {url}")

            except Exception as e:
                print(f"✖ Error processing {url}: {e}")

    # ---- WRITE INDEX ----
    if rows:
        with open(DATA_INDEX, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print("\n📁 index.csv written successfully.")


if __name__ == "__main__":
    run()
