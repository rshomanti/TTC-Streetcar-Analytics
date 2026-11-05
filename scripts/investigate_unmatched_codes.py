from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]

SUMMARY_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "incident_code_summary_with_descriptions.csv"
)

MASTER_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "ttc_master_with_routes.csv"
)

OUTPUT_DIR = PROJECT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load enriched summary
summary = pd.read_csv(SUMMARY_FILE)

# Calculate record-weighted description coverage
coverage = (
    summary.groupby("Description_Status")
    .agg(
        Incident_Records=("Incident_Count", "sum"),
        Distinct_Code_Groups=("Incident_Code", "count")
    )
    .reset_index()
)

total_records = summary["Incident_Count"].sum()

coverage["Record_Percentage"] = (
    coverage["Incident_Records"] / total_records * 100
)

coverage.to_csv(
    OUTPUT_DIR / "description_coverage.csv",
    index=False
)

print("\nDESCRIPTION COVERAGE")
print(coverage.round(2).to_string(index=False))

print(f"\nTotal records: {total_records:,}")

# Investigate MFDV records
master = pd.read_csv(
    MASTER_FILE,
    low_memory=False,
    dtype={"Incident_Code": "string"}
)

mfdv = master[
    master["Incident_Code"].str.strip().str.upper() == "MFDV"
].copy()

mfdv["Min_Delay"] = pd.to_numeric(
    mfdv["Min_Delay"], errors="coerce"
)

mfdv["Report_Date"] = pd.to_datetime(
    mfdv["Report_Date"], errors="coerce"
)

mfdv = mfdv.sort_values(
    "Min_Delay",
    ascending=False
)

mfdv.to_csv(
    OUTPUT_DIR / "mfdv_record_review.csv",
    index=False
)

print("\nMFDV RECORD REVIEW")
print(f"Total MFDV records: {len(mfdv):,}")
print(f"Average delay: {mfdv['Min_Delay'].mean():.2f}")
print(f"Median delay: {mfdv['Min_Delay'].median():.2f}")
print(f"Maximum delay: {mfdv['Min_Delay'].max():.2f}")

print("\nTOP 10 MFDV RECORDS")
columns = [
    "Report_Date",
    "Route",
    "Report_Time",
    "Location",
    "Min_Delay",
    "Min_Gap"
]

print(mfdv[columns].head(10).to_string(index=False))

print("\nFILES CREATED:")
print(OUTPUT_DIR / "description_coverage.csv")
print(OUTPUT_DIR / "mfdv_record_review.csv")