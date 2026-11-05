from pathlib import Path
import pandas as pd

# Project file paths
PROJECT_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "ttc_master_with_routes.csv"
)

OUTPUT_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "daily_summary.csv"
)

# Load the master dataset
df = pd.read_csv(
    INPUT_FILE,
    low_memory=False,
    dtype={
        "Report_Date": "string",
        "Min_Delay": "string",
        "Min_Gap": "string"
    }
)

# Convert columns to appropriate data types
df["Report_Date"] = pd.to_datetime(
    df["Report_Date"],
    errors="coerce"
)

df["Min_Delay"] = pd.to_numeric(
    df["Min_Delay"],
    errors="coerce"
)

df["Min_Gap"] = pd.to_numeric(
    df["Min_Gap"],
    errors="coerce"
)

# Remove records without a valid report date
df = df.dropna(subset=["Report_Date"])

# Group records by reporting date
daily = (
    df.groupby(df["Report_Date"].dt.date)
    .agg(
        Incident_Count=("Report_Date", "size"),
        Records_With_Valid_Delay=("Min_Delay", "count"),
        Total_Delay_Minutes=(
            "Min_Delay",
            lambda x: x.sum(min_count=1)
    ),
    Average_Delay_Minutes=("Min_Delay", "mean"),
    Median_Delay_Minutes=("Min_Delay", "median"),
    Total_Gap_Minutes=(
        "Min_Gap",
        lambda x: x.sum(min_count=1)
    )
)
    .reset_index()
)

# Rename and format date column
daily = daily.rename(
    columns={"Report_Date": "Report_Date"}
)

daily["Report_Date"] = pd.to_datetime(
    daily["Report_Date"]
)

# Sort chronologically
daily = daily.sort_values("Report_Date")

# Save aggregated dataset
daily.to_csv(OUTPUT_FILE, index=False)

# Display results
print("\nDAILY SUMMARY CREATED")
print(f"Total days: {len(daily):,}")
print(f"Date range: {daily['Report_Date'].min().date()} "
      f"to {daily['Report_Date'].max().date()}")
print(f"Output saved to: {OUTPUT_FILE}")

print("\nDAILY SUMMARY PREVIEW")
print(daily.head(10).to_string(index=False))

print("\nSUMMARY STATISTICS")
print(daily[[
    "Incident_Count",
    "Total_Delay_Minutes",
    "Average_Delay_Minutes"
]].describe().round(2).to_string())