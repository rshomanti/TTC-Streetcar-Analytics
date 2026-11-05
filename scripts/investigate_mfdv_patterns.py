from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "ttc_master_with_routes.csv"
)

OUTPUT_DIR = PROJECT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load data
df = pd.read_csv(
    INPUT_FILE,
    low_memory=False,
    dtype={
        "Incident_Code": "string",
        "Route": "string"
    }
)

df["Min_Delay"] = pd.to_numeric(
    df["Min_Delay"], errors="coerce"
)

df["Report_Date"] = pd.to_datetime(
    df["Report_Date"], errors="coerce"
)

# Filter MFDV records
mfdv = df[
    df["Incident_Code"].str.strip().str.upper() == "MFDV"
].copy()

mfdv["Year"] = mfdv["Report_Date"].dt.year
mfdv["Month"] = mfdv["Report_Date"].dt.to_period("M").astype(str)

# 1. Summary by year
year_summary = (
    mfdv.groupby("Year")
    .agg(
        Record_Count=("Record_ID", "size"),
        Total_Delay=("Min_Delay", "sum"),
        Average_Delay=("Min_Delay", "mean"),
        Median_Delay=("Min_Delay", "median"),
        Maximum_Delay=("Min_Delay", "max")
    )
    .reset_index()
)

year_summary.to_csv(
    OUTPUT_DIR / "mfdv_year_summary.csv",
    index=False
)

# 2. Summary by route
route_summary = (
    mfdv.groupby("Route", dropna=False)
    .agg(
        Record_Count=("Record_ID", "size"),
        Total_Delay=("Min_Delay", "sum"),
        Average_Delay=("Min_Delay", "mean"),
        Median_Delay=("Min_Delay", "median"),
        Maximum_Delay=("Min_Delay", "max")
    )
    .reset_index()
    .sort_values("Record_Count", ascending=False)
)

route_summary.to_csv(
    OUTPUT_DIR / "mfdv_route_summary.csv",
    index=False
)

# 3. Identify high-delay records
high_delay = mfdv[
    mfdv["Min_Delay"] >= 240
].copy()

high_delay.to_csv(
    OUTPUT_DIR / "mfdv_high_delay_records.csv",
    index=False
)

# 4. Count exact 999 and other high values
print("\nMFDV DELAY VALUE CHECK")
print(f"Total records: {len(mfdv)}")
print(f"Records with delay >= 240: {len(high_delay)}")
print(f"Records with exactly 999: {(mfdv['Min_Delay'] == 999).sum()}")
print(f"Records with delay > 999: {(mfdv['Min_Delay'] > 999).sum()}")

# 5. Display summaries
print("\nMFDV RECORDS BY YEAR")
print(year_summary.round(2).to_string(index=False))

print("\nTOP 10 ROUTES FOR MFDV")
print(route_summary.head(10).round(2).to_string(index=False))

print("\nHIGH-DELAY MFDV RECORDS")
print(
    high_delay[
        ["Report_Date", "Route", "Location", "Min_Delay", "Min_Gap"]
    ]
    .sort_values("Min_Delay", ascending=False)
    .head(15)
    .to_string(index=False)
)

print("\nFILES CREATED:")
print(OUTPUT_DIR / "mfdv_year_summary.csv")
print(OUTPUT_DIR / "mfdv_route_summary.csv")
print(OUTPUT_DIR / "mfdv_high_delay_records.csv")