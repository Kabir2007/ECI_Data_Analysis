# download.py

import os
import requests
import urllib3
from utils import rate_limit

# Suppress SSL warnings for Indian government sites
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DATA_DIR = "data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

def download_pdf(url, filename, task_id):
    rate_limit()  # 👈 ethical scraping

    # Create task-specific folder
    task_dir = os.path.join(DATA_DIR, str(task_id))
    os.makedirs(task_dir, exist_ok=True)

    try:
        response = requests.get(
            url, 
            stream=True, 
            timeout=30,  # Increased from 20 to 30
            verify=False,  # Skip SSL verification for gov sites
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        response.raise_for_status()

        filepath = os.path.join(task_dir, filename)

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=2048):
                f.write(chunk)

        return filepath
    
    except requests.exceptions.Timeout:
        print(f"⏱️  Timeout downloading: {url}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"❌ Download failed: {e}")
        raise