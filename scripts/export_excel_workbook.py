from pathlib import Path
import pandas as pd

# Project directories
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_DIR = PROJECT_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# Excel workbook destination
OUTPUT_FILE = OUTPUT_DIR / "TTC_Streetcar_Analytics.xlsx"

# CSV files and corresponding Excel worksheet names
datasets = {
    "Master Data": "ttc_master_with_routes.csv",
    "Daily Summary": "daily_summary.csv",
    "Monthly Summary": "monthly_summary.csv",
    "Yearly Summary": "yearly_summary.csv",
    "Route Summary": "route_summary.csv",
    "Route Yearly": "route_yearly_summary.csv",
    "Incident Summary": "incident_code_summary_with_descriptions.csv"
}

print("\nEXPORTING TTC DATASETS TO EXCEL")

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="xlsxwriter",
    datetime_format="yyyy-mm-dd",
    date_format="yyyy-mm-dd"
) as writer:

    for sheet_name, filename in datasets.items():

        file_path = DATA_DIR / filename

        if not file_path.exists():
            print(f"WARNING: Missing file: {filename}")
            continue

        df = pd.read_csv(file_path, low_memory=False)
        if sheet_name == "Master Data":
            df.drop(columns=["count"], errors="ignore", inplace=True)

            df["Year"] = pd.to_datetime(
                 df["Report_Date"]
            ).dt.year
        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False
        )

        # Format worksheet
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]

        header_format = workbook.add_format({
            "bold": True,
            "bg_color": "#1F4E78",
            "font_color": "white",
            "border": 1
        })

        for col_num, column_name in enumerate(df.columns):
            worksheet.write(
                0,
                col_num,
                column_name,
                header_format
            )

            # Set reasonable column widths
            sample = df[column_name].astype("string").head(1000)
            content_width = sample.str.len().max()

            width = max(
                len(str(column_name)) + 2,
                int(content_width) + 2
                if pd.notna(content_width) else 12
            )

            worksheet.set_column(
                col_num,
                col_num,
                min(width, 35)
            )

        # Freeze header row
        worksheet.freeze_panes(1, 0)

        # Add filters
        if not df.empty:
            worksheet.autofilter(
                0, 0, len(df), len(df.columns) - 1
            )

        print(
            f"Exported {sheet_name}: {len(df):,} rows"
        )

print("\nEXCEL EXPORT COMPLETE")
print(f"Workbook saved to: {OUTPUT_FILE}")