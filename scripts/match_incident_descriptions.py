from pathlib import Path
import pandas as pd
import xml.etree.ElementTree as ET

PROJECT_DIR = Path(__file__).resolve().parents[1]

REFERENCE_FILE = (
    PROJECT_DIR / "data" / "raw" / "reference"
    / "Code Descriptions.xml"
)

SUMMARY_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "incident_code_summary.csv"
)

OUTPUT_DIR = PROJECT_DIR / "data" / "processed"


# 1. Read the XML reference file
tree = ET.parse(REFERENCE_FILE)
root = tree.getroot()

reference_records = []

for row in root.findall("ROW"):
    code_element = row.find("CODE")
    description_element = row.find("DESCRIPTION")

    if code_element is None or description_element is None:
        continue

    code = code_element.text
    description = description_element.text

    if code and description:
        reference_records.append({
            "Incident_Code": code.strip().upper(),
            "Incident_Description": description.strip()
        })

reference_df = pd.DataFrame(reference_records)

# Check for duplicate codes in the reference
duplicate_codes = reference_df[
    reference_df.duplicated("Incident_Code", keep=False)
]

if not duplicate_codes.empty:
    print("\nWARNING: Duplicate codes found in reference file:")
    print(duplicate_codes.to_string(index=False))

# Keep one row per code for the matching process
reference_df = reference_df.drop_duplicates(
    subset="Incident_Code",
    keep="first"
)

# Save the reference mapping
reference_df.to_csv(
    OUTPUT_DIR / "incident_code_reference.csv",
    index=False
)


# 2. Read the incident summary
summary_df = pd.read_csv(
    SUMMARY_FILE,
    dtype={"Incident_Code": "string"}
)

# Standardize codes for matching
summary_df["Incident_Code"] = (
    summary_df["Incident_Code"]
    .str.strip()
    .str.upper()
)

# 3. Match descriptions
matched_df = summary_df.merge(
    reference_df,
    on="Incident_Code",
    how="left"
)

# 4. Identify match status
matched_df["Description_Status"] = "Matched"

missing_code = (
    matched_df["Incident_Code"] == "(MISSING CODE)"
)

matched_df.loc[
    matched_df["Incident_Description"].isna(),
    "Description_Status"
] = "Unmatched"

matched_df.loc[
    missing_code,
    "Description_Status"
] = "Missing Incident Code"

# 5. Save complete enriched summary
matched_output = OUTPUT_DIR / "incident_code_summary_with_descriptions.csv"

matched_df.to_csv(
    matched_output,
    index=False
)

# 6. Save unmatched codes separately
unmatched_df = matched_df[
    matched_df["Description_Status"] == "Unmatched"
].copy()

unmatched_output = OUTPUT_DIR / "unmatched_incident_codes.csv"

unmatched_df.to_csv(
    unmatched_output,
    index=False
)

# 7. Display results
print("\nINCIDENT DESCRIPTION MATCHING COMPLETED")

print(f"Reference descriptions: {len(reference_df)}")
print(f"Incident summary rows: {len(matched_df)}")

print(
    "Matched codes:",
    (matched_df["Description_Status"] == "Matched").sum()
)

print(
    "Unmatched codes:",
    len(unmatched_df)
)

print(
    "Missing incident code records:",
    (matched_df["Description_Status"] == "Missing Incident Code").sum()
)

print(f"\nEnriched summary saved to:\n{matched_output}")
print(f"\nUnmatched codes saved to:\n{unmatched_output}")

print("\nTOP 20 INCIDENTS WITH DESCRIPTIONS")

print(
    matched_df[
        [
            "Incident_Rank",
            "Incident_Code",
            "Incident_Description",
            "Incident_Count",
            "Total_Delay_Minutes",
            "Average_Delay_Minutes"
        ]
    ].head(20).round(2).to_string(index=False)
)