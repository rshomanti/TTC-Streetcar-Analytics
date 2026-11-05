from pathlib import Path
import pandas as pd

# Project file paths
PROJECT_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "monthly_summary.csv"
)

OUTPUT_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "yearly_summary.csv"
)

# Load monthly summary
df = pd.read_csv(INPUT_FILE)

# Convert month column
df["Month"] = pd.to_datetime(
    df["Month"],
    errors="coerce"
)

# Extract year
df["Year"] = df["Month"].dt.year

# Group records by year
yearly = (
    df.groupby("Year")
    .agg(
        Months_Reported=("Month", "nunique"),
        Reporting_Days=("Reporting_Days", "sum"),
        Incident_Count=("Incident_Count", "sum"),
        Records_With_Valid_Delay=(
            "Records_With_Valid_Delay", "sum"
        ),
        Total_Delay_Minutes=(
            "Total_Delay_Minutes",
            lambda x: x.sum(min_count=1)
        ),
        Average_Monthly_Delay=(
            "Total_Delay_Minutes", "mean"
        ),
        Total_Gap_Minutes=(
            "Total_Gap_Minutes",
            lambda x: x.sum(min_count=1)
        )
    )
    .reset_index()
)

# Calculate true weighted annual average delay
yearly["Average_Delay_Per_Record"] = (
    yearly["Total_Delay_Minutes"]
    / yearly["Records_With_Valid_Delay"]
)

# Sort chronologically
yearly = yearly.sort_values("Year")

# Save yearly summary
yearly.to_csv(OUTPUT_FILE, index=False)

# Display results
print("\nYEARLY SUMMARY CREATED")
print(f"Total years: {len(yearly):,}")
print(
    f"Year range: {yearly['Year'].min()} "
    f"to {yearly['Year'].max()}"
)
print(f"Output saved to: {OUTPUT_FILE}")

print("\nYEARLY SUMMARY PREVIEW")
print(
    yearly.round(2).to_string(index=False)
)

print("\nSUMMARY STATISTICS")
print(
    yearly[[
        "Incident_Count",
        "Total_Delay_Minutes",
        "Average_Monthly_Delay",
        "Average_Delay_Per_Record"
    ]].describe().round(2).to_string()
)