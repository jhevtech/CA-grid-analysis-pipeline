import time
import requests

def fetch_page(url, params, max_retries=3):
    """Make one EIA request. Retry server errors. Return (rows, total.)"""
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=30)
        except requests.exceptions.error as err:
            print(f"Attempt {attempt}: network error: {err}")
            time.sleep(2 ** attempt)
            continue

        if response.status_code == 200:
            body = response.json()
            if "response" not in body:
                raise ValueError(f"No data returned: {body}")
            rows = body["response"]["data"]
            total = str(body["response"]["total"])
            return rows, total

        if response.status_code >= 400:
            wait = 2 ** attempt
            print(f"Attempt {attempt}: {response.status_code}, retrying in {wait}s")
            time.sleep(wait)
            continue

        #anything else thats an error
        raise RuntimeError(f"{response.status_code}: {response.text[:200]}")

    raise RuntimeError(f"Gave up after {max_retries} attempts")