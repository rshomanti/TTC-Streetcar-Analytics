from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data" / "processed"

daily = pd.read_csv(DATA_DIR / "daily_summary.csv")
monthly = pd.read_csv(DATA_DIR / "monthly_summary.csv")
yearly = pd.read_csv(DATA_DIR / "yearly_summary.csv")

print("\nSUMMARY DATASET VALIDATION")

# Check record counts
daily_records = daily["Incident_Count"].sum()
monthly_records = monthly["Incident_Count"].sum()
yearly_records = yearly["Incident_Count"].sum()

print("\nINCIDENT COUNT RECONCILIATION")
print(f"Daily total:   {daily_records:,}")
print(f"Monthly total: {monthly_records:,}")
print(f"Yearly total:  {yearly_records:,}")

# Check valid delay record counts
daily_valid = daily["Records_With_Valid_Delay"].sum()
monthly_valid = monthly["Records_With_Valid_Delay"].sum()
yearly_valid = yearly["Records_With_Valid_Delay"].sum()

print("\nVALID DELAY RECORD RECONCILIATION")
print(f"Daily total:   {daily_valid:,}")
print(f"Monthly total: {monthly_valid:,}")
print(f"Yearly total:  {yearly_valid:,}")

# Check total delay minutes
daily_delay = daily["Total_Delay_Minutes"].sum()
monthly_delay = monthly["Total_Delay_Minutes"].sum()
yearly_delay = yearly["Total_Delay_Minutes"].sum()

print("\nTOTAL DELAY RECONCILIATION")
print(f"Daily total:   {daily_delay:,.0f}")
print(f"Monthly total: {monthly_delay:,.0f}")
print(f"Yearly total:  {yearly_delay:,.0f}")

# Check date and year coverage
print("\nDATE COVERAGE")
print(f"Daily reporting days: {len(daily):,}")
print(f"Monthly reporting periods: {len(monthly):,}")
print(f"Yearly reporting periods: {len(yearly):,}")

print("\nVALIDATION RESULTS")
print("Incident counts match:",
      daily_records == monthly_records == yearly_records)

print("Valid delay counts match:",
      daily_valid == monthly_valid == yearly_valid)

print("Total delay minutes match:",
      daily_delay == monthly_delay == yearly_delay)