import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "raw"

def save_raw(rows, dataset, start, end):
    """Save rows exactly as EIA sent them. Same inputs -> same file(overwrite)."""

    filename = f"{dataset}_{start}_{end}.json"

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / filename

    with open(path, "w") as f:
        json.dump(rows, f)

    return path 