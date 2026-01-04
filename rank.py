# rank.py

from urllib.parse import urlparse
from config import TRUSTED_DOMAINS, WEIGHT_DOMAIN_TRUST, WEIGHT_KEYWORD_MATCH

def domain_trust_score(url):
    domain = urlparse(url).netloc
    for trusted in TRUSTED_DOMAINS:
        if trusted in domain:
            return 1.0
    return 0.2  # penalty for unknown domain

def keyword_score(text, keywords):
    matches = sum(1 for k in keywords if k.lower() in text.lower())
    return matches / max(len(keywords), 1)

def score_result(item, required_keywords):
    """
    Scores a search result based on trust + relevance.
    """
    url = item.get("link", "")
    snippet = item.get("snippet", "")

    trust = domain_trust_score(url)
    relevance = keyword_score(snippet, required_keywords)

    final_score = (
        WEIGHT_DOMAIN_TRUST * trust +
        WEIGHT_KEYWORD_MATCH * relevance
    )

    return final_score
