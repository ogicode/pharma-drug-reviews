# FDA Drug Events Pipeline

A Databricks project that collects drug adverse event reports from the openFDA API as JSON, cleans and filters them, and prepares them for presentation.

## Flow

1. **Ingest** (`ingest_fda.py`): calls the openFDA API and saves the raw JSON to a volume.
2. **Bronze** (`bronze_fda.py`): loads all JSON files into a table as is.
3. **Silver** (`silver_fda.py`): cleans and types the data. Good rows go to silver, bad rows go to quarantine.
4. **Gold**: aggregated tables for reporting (planned).

## Tables

| Table | Content |
|---|---|
| `workspace.pharma.bronze_fda_events` | Raw reports |
| `workspace.pharma.silver_fda_events` | Clean reports, one row per report and drug |
| `workspace.pharma.quarantine_fda_events` | Rows with missing key fields |

## Stack

Databricks Free Edition, PySpark, Delta tables, Unity Catalog volumes, Databricks Asset Bundles

## Run

```bash
databricks bundle deploy -p ogicode
databricks bundle run ingest_fda_job -p ogicode
```

## Data source

[openFDA Drug Adverse Event API](https://open.fda.gov/apis/drug/event/)