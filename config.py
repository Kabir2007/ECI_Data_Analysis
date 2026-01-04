# config.py
'''
# ---------------------------
# API KEYS (DO NOT COMMIT)
# ---------------------------
GOOGLE_API_KEY = "AIzaSyAkC9pP5au8htBkbJBJd2uj36YUaH1Kkd0"
SEARCH_ENGINE_ID = "d78c07791f2304bbe"

# ---------------------------
# TRUSTED DOMAINS
# ---------------------------
TRUSTED_DOMAINS = [
    "gov.in",
    "nic.in",
    "eci.gov.in",
    "censusindia.gov.in",
    "mospi.gov.in",
    "rbi.org.in",
    "prsindia.org",
    "undp.org",
    "worldbank.org",
    "un.org",
    "tatatrusts.org",
    "sbi.co.in",
]

# ---------------------------
# SEARCH SETTINGS
# ---------------------------
RESULTS_PER_QUERY = 10
FILE_TYPE = "pdf"
COUNTRY = "IN"

# ---------------------------
# SCORING WEIGHTS
# ---------------------------
WEIGHT_DOMAIN_TRUST = 0.5
WEIGHT_KEYWORD_MATCH = 0.5

# ---------------------------
# GEMINI CONFIG
# ---------------------------

GEMINI_API_KEY = "AIzaSyAkC9pP5au8htBkbJBJd2uj36YUaH1Kkd0"

GEMINI_MODEL = "models/gemini-1.5-flash"

# Maximum characters to send from PDF text
GEMINI_MAX_CHARS = 12000

# ---------------------------
# SAFETY & BUDGET CONTROLS
# ---------------------------

# Seconds to wait between HTTP requests
REQUEST_DELAY_SECONDS = 2

# Max PDFs to download per domain per run
MAX_PDFS_PER_DOMAIN = 5

# Maximum PDFs processed per task (budget control)
MAX_PDFS_PER_TASK = 10

# Dry run mode (no downloads, no Gemini calls)
DRY_RUN = False


'''

# config.py

import os

# ---------------------------
# API KEYS (Use environment variables)
# ---------------------------

# config.py

# ---------------------------
# API KEYS
# ---------------------------


# Rest of your config stays the same...
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ---------------------------
# TRUSTED DOMAINS
# ---------------------------
TRUSTED_DOMAINS = [
    "gov.in",
    "nic.in",
    "eci.gov.in",
    "censusindia.gov.in",
    "mospi.gov.in",
    "rbi.org.in",
    "prsindia.org",
    "undp.org",
    "worldbank.org",
    "un.org",
    "tatatrusts.org",
    "sbi.co.in",
]

# ---------------------------
# SEARCH SETTINGS
# ---------------------------
RESULTS_PER_QUERY = 10
FILE_TYPE = "pdf"
COUNTRY = "IN"

# ---------------------------
# SCORING WEIGHTS
# ---------------------------
WEIGHT_DOMAIN_TRUST = 0.5
WEIGHT_KEYWORD_MATCH = 0.5

# ---------------------------
# GEMINI CONFIG
# ---------------------------
GEMINI_MODEL = "gemini-2.5-flash-lite"

# Maximum characters to send from PDF text
GEMINI_MAX_CHARS = 12000

# ---------------------------
# SAFETY & BUDGET CONTROLS
# ---------------------------

# Seconds to wait between HTTP requests
REQUEST_DELAY_SECONDS = 3

# Max PDFs to download per domain per run
MAX_PDFS_PER_DOMAIN = 15

# Maximum PDFs processed per task (budget control)
MAX_PDFS_PER_TASK = 25

# Dry run mode (no downloads, no Gemini calls)
DRY_RUN = False