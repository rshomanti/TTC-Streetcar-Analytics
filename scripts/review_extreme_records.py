from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_DIR / "output" / "extreme_records_review.csv"

df = pd.read_csv(DATA_FILE, low_memory=False)

df["Report_Date"] = pd.to_datetime(
    df["Report_Date"], errors="coerce"
)

df["Year"] = df["Report_Date"].dt.year

print("\nEXTREME RECORDS BY DATA PERIOD")
print(df["Data_Period"].value_counts(dropna=False))

print("\nEXTREME RECORDS BY ROUTE")
print(
    df.groupby("Route", dropna=False)
    .size()
    .sort_values(ascending=False)
    .head(20)
    .to_string()
)

print("\nEXTREME RECORDS BY LOCATION")
print(
    df.groupby("Location", dropna=False)
    .size()
    .sort_values(ascending=False)
    .head(20)
    .to_string()
)

print("\nEXTREME RECORDS BY YEAR")
print(
    df.groupby("Year")
    .size()
    .sort_values(ascending=False)
    .to_string()
)

print("\nEXTREME RECORDS BY INCIDENT DESCRIPTION")
print(
    df.groupby("Incident_Description", dropna=False)
    .size()
    .sort_values(ascending=False)
    .head(20)
    .to_string()
)