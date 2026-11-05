from pathlib import Path
import pandas as pd

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
        "Route": "string",
        "Route_Code": "string",
        "Service_Type": "string"
    }
)

# Convert delay values
df["Min_Delay"] = pd.to_numeric(
    df["Min_Delay"],
    errors="coerce"
)

# Keep regular routes only
regular = df[
    (df["Service_Type"] == "Regular") &
    (df["Mapping_Status"] == "Classified")
].copy()

# Aggregate by route
route_summary = (
    regular.groupby("Route_Code")
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

# Calculate percentage of all regular route records
total_incidents = route_summary["Incident_Count"].sum()

route_summary["Incident_Percentage"] = (
    route_summary["Incident_Count"] /
    total_incidents * 100
)

# Rank routes by incident count
route_summary = route_summary.sort_values(
    "Incident_Count",
    ascending=False
)

route_summary.insert(
    0,
    "Incident_Rank",
    range(1, len(route_summary) + 1)
)

# Save output
output_file = OUTPUT_DIR / "route_summary.csv"

route_summary.to_csv(output_file, index=False)

# Display results
print("\nROUTE SUMMARY CREATED")
print(f"Total routes: {len(route_summary)}")
print(f"Total regular route records: {total_incidents:,}")
print(f"Output saved to: {output_file}")

print("\nTOP 15 ROUTES BY INCIDENT COUNT")
print(route_summary.head(15).round(2).to_string(index=False))

print("\nROUTE SUMMARY STATISTICS")
print(
    route_summary[
        [
            "Incident_Count",
            "Total_Delay_Minutes",
            "Average_Delay_Minutes"
        ]
    ].describe().round(2).to_string()
)