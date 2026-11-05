from pathlib import Path
import pandas as pd

# Locate the project and master dataset
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_DIR / "data" / "processed" / "ttc_master_dataset.csv"

df = pd.read_csv(DATA_FILE, low_memory=False)

df["Report_Date"] = pd.to_datetime(
    df["Report_Date"], errors="coerce"
)

df["Min_Delay"] = pd.to_numeric(
    df["Min_Delay"], errors="coerce"
)

df["Min_Gap"] = pd.to_numeric(
    df["Min_Gap"], errors="coerce"
)

print("=" * 60)
print("TTC MASTER DATASET VALIDATION")
print("=" * 60)

# 1. Dataset overview
print("\n1. DATASET OVERVIEW")
print(f"Total records: {len(df):,}")
print(f"Total columns: {len(df.columns)}")
print(f"Invalid dates: {df['Report_Date'].isna().sum():,}")

print("\n2. RECORDS BY YEAR")
print(
    df.groupby(df["Report_Date"].dt.year)
      .size()
      .to_string()
)

# 2. Records by source file
print("\n3. RECORDS BY SOURCE FILE")
print(
    df.groupby("Source_File")
      .size()
      .sort_index()
      .to_string()
)

# 3. Duplicate checks
print("\n4. DUPLICATE CHECKS")
print(f"Duplicate Record_IDs: {df['Record_ID'].duplicated().sum():,}")
print(f"Exact duplicate rows: {df.duplicated().sum():,}")

# 4. Delay and gap checks
print("\n5. DELAY AND GAP CHECKS")

for column in ["Min_Delay", "Min_Gap"]:
    values = df[column].dropna()

    print(f"\n{column}")
    print(f"Missing: {df[column].isna().sum():,}")
    print(f"Negative values: {(values < 0).sum():,}")
    print(f"Zero values: {(values == 0).sum():,}")
    print(f"Minimum: {values.min()}")
    print(f"Maximum: {values.max()}")
    print("Percentiles:")
    print(values.quantile([0.50, 0.75, 0.90, 0.95, 0.99]).to_string())

# 5. Route checks
print("\n6. ROUTE CHECKS")
print(f"Unique route labels: {df['Route'].nunique(dropna=True)}")
print(f"Missing routes: {df['Route'].isna().sum():,}")

print("\nMost common route labels:")
print(df["Route"].value_counts(dropna=False).head(40).to_string())

# 6. Time checks
print("\n7. TIME CHECKS")
print("Most common reported times:")
print(df["Report_Time"].value_counts().head(15).to_string())

print("\nVALIDATION COMPLETE")