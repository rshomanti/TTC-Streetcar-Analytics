from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]

MASTER_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "ttc_master_dataset.csv"
)

MAPPING_FILE = (
    PROJECT_DIR / "output" / "route_mapping.csv"
)

OUTPUT_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "ttc_master_with_routes.csv"
)

# Load datasets
master = pd.read_csv(
    MASTER_FILE,
    low_memory=False,
    dtype={
        "Record_ID": "string",
        "Route": "string",
        "Incident_Code": "string",
        "Incident_Description": "string"
    }
)
mapping = pd.read_csv(MAPPING_FILE)

# Standardize route labels for matching
master["Route_Key"] = (
    master["Route"]
    .fillna("MISSING")
    .astype(str)
    .str.strip()
    .str.upper()
)

mapping["Route_Key"] = (
    mapping["Original_Route"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Keep mapping columns
mapping = mapping[
    [
        "Route_Key",
        "Route_Code",
        "Service_Type",
        "Mapping_Status",
        "Notes"
    ]
]

# Join mapping to master dataset
master = master.merge(
    mapping,
    on="Route_Key",
    how="left",
    validate="many_to_one"
)

# Rename notes column
master = master.rename(
    columns={"Notes": "Route_Notes"}
)

# Remove temporary matching field
master = master.drop(columns=["Route_Key"])

# Save
master.to_csv(OUTPUT_FILE, index=False)

print("\nROUTE MAPPING APPLIED")
print(f"Total records: {len(master):,}")
print(f"Output saved to: {OUTPUT_FILE}")

print("\nSERVICE TYPE RECORD COUNTS")
print(
    master["Service_Type"]
    .value_counts(dropna=False)
    .to_string()
)

print("\nMAPPING STATUS")
print(
    master["Mapping_Status"]
    .value_counts(dropna=False)
    .to_string()
)