from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_DIR / "data" / "processed" / "ttc_master_dataset.csv"
OUTPUT_DIR = PROJECT_DIR / "output"

df = pd.read_csv(DATA_FILE, low_memory=False)

# Count original route labels
route_counts = (
    df["Route"]
    .fillna("MISSING")
    .value_counts()
    .reset_index()
)

route_counts.columns = ["Original_Route", "Record_Count"]

# Add percentage of total records
route_counts["Percentage"] = (
    route_counts["Record_Count"] / len(df) * 100
).round(2)

# Save the complete route-label review
output_file = OUTPUT_DIR / "route_label_frequency.csv"

route_counts.to_csv(output_file, index=False)

print("\nTOTAL DISTINCT ROUTE LABELS:")
print(df["Route"].nunique())

print("\nTOP 40 ROUTE LABELS:")
print(route_counts.head(40).to_string(index=False))

print("\nROUTE LABEL REVIEW SAVED:")
print(output_file)