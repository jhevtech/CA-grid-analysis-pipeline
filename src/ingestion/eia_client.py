import time
import requests

def fetch_page(url, params, max_retries=3):
    """Make one EIA request. Retry server errors. Return (rows, total.)"""
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=30)
        except requests.exceptions.RequestException as err:
            print(f"Attempt {attempt}: network error: {err}")
            time.sleep(2 ** attempt)
            continue

        if response.status_code == 200:
            body = response.json()
            if "response" not in body:
                raise ValueError(f"No data returned: {body}")
            rows = body["response"]["data"]
            total = int(body["response"]["total"])
            return rows, total

        if response.status_code >= 400:
            wait = 2 ** attempt
            print(f"Attempt {attempt}: {response.status_code}, retrying in {wait}s")
            time.sleep(wait)
            continue

        #anything else thats an error
        raise RuntimeError(f"{response.status_code}: {response.text[:200]}")

    raise RuntimeError(f"Gave up after {max_retries} attempts")


def fetch_all(url, params, page_size=5000):
    """Return one combined list after paging througn every matching row"""
    all_rows = []
    offset = 0
    total = None

    while total is None or offset < total:
        page_params = params.copy()
        page_params["offset"] = offset
        page_params["length"] = page_size
        page_params["sort[0][column]"] = "period"
        page_params["sort[0][direction]"] = "asc"

        rows, total = fetch_page(url, page_params)

        if total == 0:
            raise ValueError("0 rows matched. Check facets and datas.")
        if not rows:
            break

        all_rows.extend(rows)
        offset += page_size
        print(f"Fetched {len(all_rows)} / {total}")

    return all_rows