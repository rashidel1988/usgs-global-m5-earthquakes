"""Fetch a reproducible snapshot of M5+ earthquakes from the USGS ComCat API."""

from __future__ import annotations

import csv
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://earthquake.usgs.gov/fdsnws/event/1/query"
PARAMS = {
    "format": "csv",
    "starttime": "2016-01-01",
    "endtime": "2025-12-31T23:59:59.999",
    "minmagnitude": 5,
    "eventtype": "earthquake",
    "orderby": "time-asc",
}
OUT = Path(__file__).with_name("earthquakes_m5_2016_2025.csv")
SNAPSHOT = Path(__file__).with_name("snapshot-info.json")


def fetch() -> tuple[list[str], list[dict[str, str]]]:
    url = f"{API}?{urlencode(PARAMS)}"
    request = Request(url, headers={"User-Agent": "quake-catalog-community-dataset/1.0"})
    with urlopen(request, timeout=120) as response:
        text = response.read().decode("utf-8-sig")
    if text.lstrip().startswith("#"):
        raise RuntimeError(f"USGS returned a message instead of CSV: {text[:500]}")

    reader = csv.DictReader(io.StringIO(text))
    fieldnames = reader.fieldnames
    if not fieldnames:
        raise RuntimeError("USGS response did not contain a CSV header.")
    required = {"time", "latitude", "longitude", "depth", "mag", "id", "place"}
    missing = required.difference(fieldnames)
    if missing:
        raise RuntimeError(f"USGS response is missing expected columns: {sorted(missing)}")

    rows: dict[str, dict[str, str]] = {}
    for row in reader:
        try:
            datetime.fromisoformat(row["time"].replace("Z", "+00:00"))
            float(row["latitude"])
            float(row["longitude"])
            float(row["mag"])
        except (ValueError, TypeError):
            continue
        if row["id"]:
            rows[row["id"]] = row

    ordered = sorted(
        rows.values(),
        key=lambda row: datetime.fromisoformat(row["time"].replace("Z", "+00:00")),
    )
    with OUT.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ordered)
    snapshot = {
        "source": "U.S. Geological Survey (USGS), ComCat earthquake catalog",
        "api": API,
        "downloaded_utc": datetime.now(timezone.utc).isoformat(),
        "query": PARAMS,
        "row_count": len(ordered),
        "sort_order": "time ascending",
        "deduplication": "USGS event id; last returned record retained",
    }
    SNAPSHOT.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    return fieldnames, ordered


if __name__ == "__main__":
    _, earthquakes = fetch()
    print(f"Wrote {len(earthquakes):,} events to {OUT.name}")
    print(f"Snapshot details written to {SNAPSHOT.name}")
