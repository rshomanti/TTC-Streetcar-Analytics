from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_DIR / "data" / "processed" / "ttc_master_dataset.csv"
OUTPUT_DIR = PROJECT_DIR / "output"

df = pd.read_csv(DATA_FILE, low_memory=False)

for col in ["Min_Delay", "Min_Gap"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --------------------------------------------------
# 1. FREQUENCY OF EXACT 999 VALUES
# --------------------------------------------------

print("=" * 60)
print("EXACT 999 VALUE INVESTIGATION")
print("=" * 60)

for col in ["Min_Delay", "Min_Gap"]:
    print(f"\n{col}")
    print(f"Exactly 999: {(df[col] == 999).sum():,}")
    print(f"Between 990 and 1000: {df[col].between(990, 1000).sum():,}")
    print(f"Above 999: {(df[col] > 999).sum():,}")

# --------------------------------------------------
# 2. EXTREME VALUES BY SOURCE FILE
# --------------------------------------------------

print("\n" + "=" * 60)
print("EXTREME VALUES BY SOURCE")
print("=" * 60)

for col in ["Min_Delay", "Min_Gap"]:
    print(f"\n{col}: records above 240 minutes")

    extreme = df[df[col] > 240]

    print(
        extreme.groupby("Source_File")
        .agg(
            Records=(col, "size"),
            Average=(col, "mean"),
            Maximum=(col, "max")
        )
        .sort_values("Records", ascending=False)
        .to_string()
    )

# --------------------------------------------------
# 3. EXTREME DELAYS BY INCIDENT DESCRIPTION
# --------------------------------------------------

print("\n" + "=" * 60)
print("HIGH DELAYS BY INCIDENT DESCRIPTION")
print("=" * 60)

high_delay = df[df["Min_Delay"] > 240]

print(
    high_delay.groupby("Incident_Description", dropna=False)
    .agg(
        Records=("Min_Delay", "size"),
        Average_Delay=("Min_Delay", "mean"),
        Maximum_Delay=("Min_Delay", "max")
    )
    .sort_values("Records", ascending=False)
    .head(20)
    .to_string()
)

# --------------------------------------------------
# 4. HIGH DELAYS BY YEAR
# --------------------------------------------------

print("\n" + "=" * 60)
print("HIGH DELAYS BY YEAR")
print("=" * 60)

df["Report_Date"] = pd.to_datetime(df["Report_Date"], errors="coerce")
df["Year"] = df["Report_Date"].dt.year

print(
    df.groupby("Year")
    .agg(
        Total_Records=("Min_Delay", "size"),
        Delays_Above_240=("Min_Delay", lambda x: (x > 240).sum()),
        Delays_Exactly_999=("Min_Delay", lambda x: (x == 999).sum()),
        Maximum_Delay=("Min_Delay", "max")
    )
    .to_string()
)

# --------------------------------------------------
# 5. SAVE ALL EXTREME RECORDS FOR REVIEW
# --------------------------------------------------

extreme_records = df[
    (df["Min_Delay"] > 240) |
    (df["Min_Gap"] > 240)
].copy()

extreme_records.to_csv(
    OUTPUT_DIR / "extreme_records_review.csv",
    index=False
)

print("\nSaved: output/extreme_records_review.csv")
print(f"Total records flagged for review: {len(extreme_records):,}")

print("\nINVESTIGATION COMPLETE")