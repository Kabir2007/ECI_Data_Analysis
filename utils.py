# utils.py

import time
import hashlib
import os
from urllib.parse import urlparse
from config import REQUEST_DELAY_SECONDS, MAX_PDFS_PER_DOMAIN


# ---------------------------
# RATE LIMITING
# ---------------------------

def rate_limit():
    time.sleep(REQUEST_DELAY_SECONDS)


# ---------------------------
# DOMAIN TRACKING
# ---------------------------

domain_counter = {}

def domain_allowed(url):
    domain = urlparse(url).netloc
    count = domain_counter.get(domain, 0)

    if count >= MAX_PDFS_PER_DOMAIN:
        return False

    domain_counter[domain] = count + 1
    return True


# ---------------------------
# PDF DEDUPLICATION
# ---------------------------

def sha256_file(filepath):
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha.update(chunk)
    return sha.hexdigest()


# ---------------------------
# BASIC PDF VALIDATION
# ---------------------------

def is_valid_pdf(filepath):
    try:
        with open(filepath, "rb") as f:
            header = f.read(4)
            return header == b"%PDF"
    except:
        return False



