from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
HISTORICAL_DIR = PROJECT_DIR / "data" / "raw" / "historical"
RECENT_DIR = PROJECT_DIR / "data" / "raw" / "recent"

print("TTC STREETCAR DATA SUMMARY")
print("=" * 60)

# Historical Excel files
historical_files = sorted(HISTORICAL_DIR.glob("*.xls*"))

print(f"\nHistorical files found: {len(historical_files)}")

for file in historical_files:
    try:
        excel = pd.ExcelFile(file)

        for sheet in excel.sheet_names:
            df = pd.read_excel(file, sheet_name=sheet)

            print(f"\nFILE: {file.name}")
            print(f"Sheet: {sheet}")
            print(f"Rows: {len(df):,}")
            print(f"Columns: {df.columns.tolist()}")

            if "Date" in df.columns:
                dates = pd.to_datetime(df["Date"], errors="coerce")
                print(f"Date range: {dates.min()} to {dates.max()}")

            print("Missing values:")
            print(df.isnull().sum().to_dict())

    except Exception as error:
        print(f"\nERROR reading {file.name}: {error}")

# Recent XML files
recent_files = sorted(RECENT_DIR.glob("*.xml"))

print(f"\n\nRecent XML files found: {len(recent_files)}")

for file in recent_files:
    try:
        df = pd.read_xml(file, xpath=".//ROW")

        print(f"\nFILE: {file.name}")
        print(f"Rows: {len(df):,}")
        print(f"Columns: {df.columns.tolist()}")

        if "Date" in df.columns:
            dates = pd.to_datetime(df["Date"], errors="coerce")
            print(f"Date range: {dates.min()} to {dates.max()}")

        print("Missing values:")
        print(df.isnull().sum().to_dict())

    except Exception as error:
        print(f"\nERROR reading {file.name}: {error}")

print("\nDATA INSPECTION COMPLETE")