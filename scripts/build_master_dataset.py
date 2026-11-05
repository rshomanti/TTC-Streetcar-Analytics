
from pathlib import Path
import pandas as pd

# Project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent

HISTORICAL_DIR = PROJECT_DIR / "data" / "raw" / "historical"
RECENT_DIR = PROJECT_DIR / "data" / "raw" / "recent"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Standardize different versions of column names
COLUMN_MAP = {
    "report date": "Report_Date",
    "date": "Report_Date",
    "route": "Route",
    "line": "Route",
    "time": "Report_Time",
    "day": "Day_of_Week",
    "location": "Location",
    "station": "Location",
    "incident": "Incident_Description",
    "incident id": "Incident_ID",
    "code": "Incident_Code",
    "min delay": "Min_Delay",
    "delay": "Min_Delay",
    "mindelay": "Min_Delay",
    "min gap": "Min_Gap",
    "gap": "Min_Gap",
    "mingap": "Min_Gap",
    "direction": "Direction",
    "bound": "Direction",
    "vehicle": "Vehicle_ID",
    "_id": "Record_ID"
}


def standardize_columns(df):
    rename_columns = {}

    for column in df.columns:
        cleaned_name = str(column).strip().lower()
        if cleaned_name in COLUMN_MAP:
            rename_columns[column] = COLUMN_MAP[cleaned_name]

    return df.rename(columns=rename_columns)


all_data = []

# --------------------------------
# 1. Read historical Excel files
# --------------------------------

historical_files = sorted(HISTORICAL_DIR.glob("*.xls*"))

print(f"Historical files found: {len(historical_files)}")

for file in historical_files:

    print(f"Reading: {file.name}")

    try:
        excel = pd.ExcelFile(file)

        for sheet in excel.sheet_names:

            df = pd.read_excel(file, sheet_name=sheet)

            df = standardize_columns(df)

            df["Source_File"] = file.name
            df["Source_Sheet"] = sheet
            df["Data_Period"] = "Historical"

            all_data.append(df)

            print(f"  {sheet}: {len(df):,} records")

    except Exception as error:
        print(f"ERROR reading {file.name}: {error}")


# --------------------------------
# 2. Read recent XML files
# --------------------------------

recent_files = sorted(RECENT_DIR.glob("*.xml"))

print(f"\nRecent XML files found: {len(recent_files)}")

for file in recent_files:

    print(f"Reading: {file.name}")

    try:
        df = pd.read_xml(file, xpath=".//ROW")
        print("\nXML columns:")
        print(df.columns.tolist())

        print("\nFirst 10 count values:")
        print(df["count"].head(10))

        df = standardize_columns(df)

        df["Source_File"] = file.name
        df["Source_Sheet"] = "XML"
        df["Data_Period"] = "Recent"

        all_data.append(df)

        print(f"  Records: {len(df):,}")

    except Exception as error:
        print(f"ERROR reading {file.name}: {error}")


# --------------------------------
# 3. Combine all records
# --------------------------------

if not all_data:
    raise ValueError("No data was loaded. Check your raw data folders.")

master_df = pd.concat(all_data, ignore_index=True, sort=False)

# Ensure expected columns exist
expected_columns = [
    "Record_ID",
    "Report_Date",
    "Route",
    "Report_Time",
    "Day_of_Week",
    "Location",
    "Incident_Code",
    "Incident_Description",
    "Incident_ID",
    "Min_Delay",
    "Min_Gap",
    "Direction",
    "Vehicle_ID",
    "Data_Period",
    "Source_File",
    "Source_Sheet"
]

for column in expected_columns:
    if column not in master_df.columns:
        master_df[column] = pd.NA

# Convert date and numeric columns
master_df["Report_Date"] = pd.to_datetime(
    master_df["Report_Date"],
    errors="coerce"
)

for column in ["Min_Delay", "Min_Gap"]:
    master_df[column] = pd.to_numeric(
        master_df[column],
        errors="coerce"
    )

# Convert all record IDs to text first
master_df["Record_ID"] = master_df["Record_ID"].astype("string")

# Identify records without an ID
missing_id = master_df["Record_ID"].isna()

# Generate unique IDs for historical records
master_df.loc[missing_id, "Record_ID"] = [
    f"HIST-{i:08d}" for i in range(missing_id.sum())
]

# Put standardized columns first
master_df = master_df[
    expected_columns +
    [
        col for col in master_df.columns
        if col not in expected_columns
    ]
]

# --------------------------------
# 4. Export master dataset
# --------------------------------

output_file = OUTPUT_DIR / "ttc_master_dataset.csv"

master_df.to_csv(output_file, index=False)

# --------------------------------
# 5. Print summary
# --------------------------------

print("\n" + "=" * 60)
print("MASTER DATASET CREATED")
print("=" * 60)

print(f"Total records: {len(master_df):,}")
print(f"Total columns: {len(master_df.columns)}")

print("\nDate range:")
print(master_df["Report_Date"].min())
print("to")
print(master_df["Report_Date"].max())

print("\nRecords by data period:")
print(master_df["Data_Period"].value_counts())

print("\nMissing values:")
print(master_df[expected_columns].isna().sum())

print("\nOutput saved to:")
print(output_file)

print("\nDATA PROCESSING COMPLETE")