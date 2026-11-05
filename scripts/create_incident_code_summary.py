from pathlib import Path
import pandas as pd

# Project directory
PROJECT_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "ttc_master_with_routes.csv"
)

OUTPUT_DIR = PROJECT_DIR / "data" / "processed"

# Load dataset
df = pd.read_csv(
    INPUT_FILE,
    low_memory=False,
    dtype={
        "Incident_Code": "string",
        "Data_Period": "string"
    }
)

# Convert delay values to numeric
df["Min_Delay"] = pd.to_numeric(
    df["Min_Delay"],
    errors="coerce"
)

# Keep recent records only (2025 onward)
recent = df[
    df["Data_Period"] == "Recent"
].copy()

# Group by incident code, retaining records with missing codes
incident_summary = (
    recent.groupby("Incident_Code", dropna=False)
    .agg(
        Incident_Count=("Record_ID", "size"),
        Total_Delay_Minutes=(
            "Min_Delay",
            lambda x: x.sum(min_count=1)
        ),
        Average_Delay_Minutes=("Min_Delay", "mean"),
        Median_Delay_Minutes=("Min_Delay", "median"),
        Maximum_Delay_Minutes=("Min_Delay", "max"),
        Records_With_Valid_Delay=("Min_Delay", "count")
    )
    .reset_index()
)

# Label missing incident codes
incident_summary["Incident_Code"] = (
    incident_summary["Incident_Code"]
    .fillna("(Missing code)")
)

# Calculate percentage of all recent records
total_records = len(recent)

incident_summary["Incident_Percentage"] = (
    incident_summary["Incident_Count"]
    / total_records * 100
)

# Rank by incident frequency
incident_summary = incident_summary.sort_values(
    "Incident_Count",
    ascending=False
).reset_index(drop=True)

incident_summary.insert(
    0,
    "Incident_Rank",
    range(1, len(incident_summary) + 1)
)

# Save output
output_file = OUTPUT_DIR / "incident_code_summary.csv"

incident_summary.to_csv(
    output_file,
    index=False
)

# Display results
print("\nINCIDENT CODE SUMMARY CREATED")
print(f"Total recent records: {total_records:,}")
print(f"Distinct incident codes: {recent['Incident_Code'].nunique()}")
print(f"Output saved to: {output_file}")

print("\nTOP 20 INCIDENT CODES")
print(
    incident_summary.head(20)
    .round(2)
    .to_string(index=False)
)

print("\nINCIDENT SUMMARY STATISTICS")
print(
    incident_summary[
        [
            "Incident_Count",
            "Total_Delay_Minutes",
            "Average_Delay_Minutes"
        ]
    ].describe().round(2).to_string()
)

print("\nMISSING INCIDENT CODE RECORDS")
print(
    recent["Incident_Code"].isna().sum()
)