import pandas as pd
from src.ingestion.eia_client import fetch_all, NoDataError
from src.ingestion.raw_storage import save_raw, raw_path


def month_ranges(first="2015-07-01"):
    """Return (start, end) strings for every month from `first` to now."""
    ranges = []
    for s in pd.date_range(first, pd.Timestamp.today(), freq="MS"):
        e = s + pd.offsets.MonthEnd(1)                  # last day of that month
        ranges.append((s.strftime("%Y-%m-%dT00"), e.strftime("%Y-%m-%dT23")))
    return ranges


def backfill(dataset, url, params, first="2015-07-01"):
    ranges = month_ranges(first)
    recent = {r[0] for r in range[-2:]}                   # the last month = this month

    for start, end in ranges:
        path = raw_path(dataset, start, end)
        if path.exists() and start != recent:     # already have it
            print(f"{dataset} {start[:7]}: exists, skipping")
            continue

        p = params.copy()
        p["start"] = start
        p["end"] = end

        try:
            rows = fetch_all(url, p)
        except NoDataError:                                  # the zero-row error from fetch_all
            print(f"{dataset} {start[:7]}: no data, skipping")
            continue

        save_raw(rows, dataset, start, end)
        print(f"{dataset} {start[:7]}: saved {len(rows)} rows")