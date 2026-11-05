from pathlib import Path
import pandas as pd

# Project file paths
PROJECT_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "daily_summary.csv"
)

OUTPUT_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "monthly_summary.csv"
)

# Load daily summary
df = pd.read_csv(INPUT_FILE)

# Convert date column
df["Report_Date"] = pd.to_datetime(
    df["Report_Date"],
    errors="coerce"
)

# Create monthly period
df["Month"] = (
    df["Report_Date"].dt.to_period("M")
)

# Group records by month
monthly = (
    df.groupby("Month")
    .agg(
        Reporting_Days=("Report_Date", "nunique"),
        Incident_Count=("Incident_Count", "sum"),
        Records_With_Valid_Delay=(
            "Records_With_Valid_Delay", "sum"
        ),
        Total_Delay_Minutes=(
            "Total_Delay_Minutes",
            lambda x: x.sum(min_count=1)
        ),
        Average_Daily_Delay=(
            "Total_Delay_Minutes", "mean"
        ),
        Total_Gap_Minutes=(
            "Total_Gap_Minutes",
            lambda x: x.sum(min_count=1)
        )
    )
    .reset_index()
)

# Calculate true weighted average delay per record
monthly["Average_Delay_Per_Record"] = (
    monthly["Total_Delay_Minutes"]
    / monthly["Records_With_Valid_Delay"]
)

# Format month as date
monthly["Month"] = (
    monthly["Month"].dt.to_timestamp()
)

# Sort chronologically
monthly = monthly.sort_values("Month")

# Save monthly summary
monthly.to_csv(OUTPUT_FILE, index=False)

# Display results
print("\nMONTHLY SUMMARY CREATED")
print(f"Total months: {len(monthly):,}")
print(
    f"Date range: {monthly['Month'].min().date()} "
    f"to {monthly['Month'].max().date()}"
)
print(f"Output saved to: {OUTPUT_FILE}")

print("\nMONTHLY SUMMARY PREVIEW")
print(
    monthly.head(10).to_string(
        index=False,
        formatters={
            "Average_Daily_Delay": "{:.2f}".format,
            "Average_Delay_Per_Record": "{:.2f}".format
        }
    )
)
print("\nSUMMARY STATISTICS")
print(
    monthly[[
        "Incident_Count",
        "Total_Delay_Minutes",
        "Average_Daily_Delay",
        "Average_Delay_Per_Record"
    ]].describe().round(2).to_string()
)