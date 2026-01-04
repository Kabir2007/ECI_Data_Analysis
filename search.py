# search.py

import requests
from config import GOOGLE_API_KEY, SEARCH_ENGINE_ID, FILE_TYPE, COUNTRY, RESULTS_PER_QUERY

BASE_URL = "https://www.googleapis.com/customsearch/v1"

def google_search(query):
    """
    Performs a Google Custom Search query and returns raw results.
    """
    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "fileType": FILE_TYPE,
        "gl": COUNTRY,
        "num": RESULTS_PER_QUERY
    }

    print(f"Searching: {query}")
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        return response.json().get("items", [])
    except requests.exceptions.Timeout:
        print(f"⏱️  Search timeout for: {query}")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        return []
    except Exception as e:
        print(f"❌ Search error: {e}")
        return []