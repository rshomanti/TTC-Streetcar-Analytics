from pathlib import Path
import pandas as pd

# Project paths
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_DIR / "data" / "processed" / "ttc_master_dataset.csv"
OUTPUT_DIR = PROJECT_DIR / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE, low_memory=False)

# Convert numerical columns
df["Min_Delay"] = pd.to_numeric(df["Min_Delay"], errors="coerce")
df["Min_Gap"] = pd.to_numeric(df["Min_Gap"], errors="coerce")

# --------------------------------------------------
# 1. INVESTIGATE HIGH DELAY RECORDS
# --------------------------------------------------

print("=" * 60)
print("HIGH DELAY RECORDS")
print("=" * 60)

print("\nTop 25 records by delay:")

delay_columns = [
    "Report_Date", "Route", "Location",
    "Incident_Description", "Incident_Code",
    "Min_Delay", "Min_Gap", "Source_File"
]

top_delays = df.nlargest(25, "Min_Delay")[delay_columns]

print(top_delays.to_string(index=False))

top_delays.to_csv(
    OUTPUT_DIR / "high_delay_records.csv",
    index=False
)

# --------------------------------------------------
# 2. INVESTIGATE HIGH GAP RECORDS
# --------------------------------------------------

print("\n" + "=" * 60)
print("HIGH GAP RECORDS")
print("=" * 60)

top_gaps = df.nlargest(25, "Min_Gap")[delay_columns]

print(top_gaps.to_string(index=False))

top_gaps.to_csv(
    OUTPUT_DIR / "high_gap_records.csv",
    index=False
)

# --------------------------------------------------
# 3. INVESTIGATE ROUTE LABELS
# --------------------------------------------------

print("\n" + "=" * 60)
print("ROUTE LABEL REVIEW")
print("=" * 60)

route_counts = (
    df["Route"]
    .fillna("MISSING")
    .value_counts()
    .rename_axis("Original_Route")
    .reset_index(name="Record_Count")
)

# Extract a possible three-digit route number.
# Keep the original label for reference.
route_counts["Possible_Route_Code"] = (
    route_counts["Original_Route"]
    .str.extract(r"^\s*(\d{3})(?:\.0)?(?:\b|$)", expand=False)
)

route_counts.to_csv(
    OUTPUT_DIR / "route_label_review.csv",
    index=False
)

print(f"\nUnique route labels: {df['Route'].nunique(dropna=True)}")
print("\nMost common route labels:")
print(route_counts.head(40).to_string(index=False))

print("\nRoute labels with fewer than 20 records:")
print(
    route_counts[
        route_counts["Record_Count"] < 20
    ].to_string(index=False)
)

# --------------------------------------------------
# 4. SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("INVESTIGATION FILES CREATED")
print("=" * 60)

print("output/high_delay_records.csv")
print("output/high_gap_records.csv")
print("output/route_label_review.csv")

print("\nINVESTIGATION COMPLETE")