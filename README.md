# Global M5+ Earthquakes, 2016–2025

A documented, reproducible snapshot of global magnitude 5.0 and larger earthquake records from the USGS ComCat catalog. The extract contains **17,502 events** returned by the query saved in snapshot-info.json. Records are sorted by origin time in UTC and de-duplicated by the USGS event ID.

## Published on Kaggle

- [Dataset: USGS Global M5+ Earthquakes, 2016–2025](https://www.kaggle.com/datasets/rashidel1988/usgs-global-m5-earthquakes-2016-2025)
- [R notebook: Global M5+ Earthquakes: R Exploration](https://www.kaggle.com/code/rashidel1988/global-m5-earthquakes-r-exploration)
- R Markdown report source: [USGS M5+ Catalog Data Quality and Coverage Audit](usgs_catalog_audit.Rmd)

The CSV is published on Kaggle. This GitHub repository keeps the extraction code, snapshot metadata, and analysis notebook; it does not redistribute the catalog records. Run **python fetch_catalog.py** to retrieve a fresh local copy from USGS, subject to the source and reuse notes below.

## Files

| File | Contents |
|---|---|
| earthquakes_m5_2016_2025.csv | Generated locally by the refresh script; the published snapshot is on Kaggle |
| snapshot-info.json | Retrieval time, query parameters, row count, and extraction notes |
| fetch_catalog.py | Small standard-library script for refreshing the same time window |
| earthquakes_r_notebook.ipynb | R notebook for basic checks, magnitude and depth views, and annual counts |
| usgs_catalog_audit.Rmd | R Markdown report auditing record integrity, missingness, magnitude types, and network coverage |
| dataset-cover-image.png | Equirectangular event-coordinate plot generated from the snapshot; it has no basemap |

## Fields

The CSV uses the field names returned by the USGS API.

| Field | Meaning |
|---|---|
| time | Preferred origin time in UTC |
| latitude, longitude | Preferred epicenter coordinates in decimal degrees |
| depth | Preferred hypocenter depth in kilometers |
| mag, magType | Preferred magnitude value and its reported magnitude scale |
| nst | Number of stations used for the preferred origin, when reported |
| gap | Largest azimuthal gap between stations, in degrees |
| dmin | Distance to the nearest station, in degrees |
| rms | Root-mean-square travel-time residual, in seconds |
| net, locationSource, magSource | Network and source codes supplied for the event, location, and magnitude |
| id | USGS event identifier |
| updated | Time the catalog record was last updated, in UTC |
| place | USGS human-readable location description |
| type | Event type; filtered to earthquake |
| horizontalError, depthError, magError | Reported uncertainty values, where available |
| magNst | Number of stations used for the magnitude, when reported |
| status | Review status supplied by the catalog |

Blank values mean a field was not supplied for that event. Numeric values describe the preferred catalog solution and can change when the source record is revised.

## Reproduce the extract

Run **python fetch_catalog.py**. The script requests the USGS FDSN CSV format for the fixed UTC interval 2016-01-01 through 2025-12-31, filters to earthquake events with magnitude at least 5.0, validates the essential columns, removes duplicate event IDs, and writes the CSV and snapshot metadata. It uses only Python's standard library.

## Interpretation

This is a thresholded catalog extract, not a complete record of every earthquake. It omits events below magnitude 5.0 and the catalog's detection, review, and contributing network coverage can vary over time. Annual counts should not be interpreted as a direct measure of changes in the Earth's underlying earthquake rate. Magnitude scales differ; use magType when comparing values. See the [USGS catalog documentation](https://earthquake.usgs.gov/fdsnws/event/1/) for query details and field definitions.

## Source and reuse

Source: U.S. Geological Survey (USGS), [ComCat event catalog](https://earthquake.usgs.gov/earthquakes/search/) through the [FDSN Event Web Service](https://earthquake.usgs.gov/fdsnws/event/1/). USGS requests source credit. ComCat may include records contributed by other networks, so this package does not apply a blanket license to every source record. The Kaggle license is marked **Other** to point to these source conditions; check applicable terms before redistributing individual contributed records or using them commercially. See [USGS data licensing](https://www.usgs.gov/data-management/data-licensing) and [USGS credit guidance](https://www.usgs.gov/information-policies-and-instructions/acknowledging-or-crediting-usgs).

The original extraction script and notebook in this repository are dedicated to the public domain under CC0. This dedication applies to those authored code files, not to source catalog records.
