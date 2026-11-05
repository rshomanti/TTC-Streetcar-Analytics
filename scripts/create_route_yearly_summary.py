from pathlib import Path
import pandas as pd

# Project directory
PROJECT_DIR = Path(__file__).resolve().parents[1]

# Input and output files
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

# Convert columns to appropriate data types
df["Report_Date"] = pd.to_datetime(
    df["Report_Date"], errors="coerce"
)

df["Min_Delay"] = pd.to_numeric(
    df["Min_Delay"], errors="coerce"
)

# Extract year
df["Year"] = df["Report_Date"].dt.year

# Keep classified regular streetcar routes
regular = df[
    (df["Service_Type"] == "Regular") &
    (df["Mapping_Status"] == "Classified") &
    (df["Year"].notna())
].copy()

# Group by year and route
route_yearly_summary = (
    regular.groupby(["Year", "Route_Code"])
    .agg(
        Incident_Count=("Record_ID", "size"),
        Total_Delay_Minutes=(
            "Min_Delay",
            lambda x: x.sum(min_count=1)
        ),
        Average_Delay_Minutes=("Min_Delay", "mean"),
        Median_Delay_Minutes=("Min_Delay", "median"),
        Records_With_Valid_Delay=("Min_Delay", "count")
    )
    .reset_index()
)

# Sort by year and route
route_yearly_summary = route_yearly_summary.sort_values(
    ["Year", "Route_Code"]
)

# Save output
output_file = OUTPUT_DIR / "route_yearly_summary.csv"

route_yearly_summary.to_csv(
    output_file,
    index=False
)

# Display results
print("\nROUTE YEARLY SUMMARY CREATED")
print(f"Total records: {len(regular):,}")
print(f"Total routes: {regular['Route_Code'].nunique()}")
print(f"Years covered: {regular['Year'].nunique()}")
print(f"Output saved to: {output_file}")

print("\nSUMMARY PREVIEW")
print(
    route_yearly_summary.head(20).round(2).to_string(index=False)
)

print("\nRECORD COUNTS BY YEAR")
print(
    route_yearly_summary.groupby("Year")["Incident_Count"]
    .sum()
    .to_string()
)