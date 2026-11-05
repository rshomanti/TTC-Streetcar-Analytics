from pathlib import Path
import pandas as pd
import re

PROJECT_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = PROJECT_DIR / "output" / "route_label_frequency.csv"
OUTPUT_FILE = PROJECT_DIR / "output" / "route_mapping.csv"

routes = pd.read_csv(INPUT_FILE)

# Standard daytime streetcar routes
DAY_ROUTES = {
    "501", "502", "503", "504", "505", "506",
    "507", "508", "509", "510", "511", "512", "514"
}

# Known night-service route numbers
NIGHT_ROUTES = {
    "301", "303", "304", "305", "306",
    "307", "309", "310", "311", "312"
}

# Confirmed descriptive aliases from our review
ALIASES = {
    "501 QUEEN": "501",
    "504 KING": "504",
    "503 KINGSTON ROAD": "503",
    "503 KINGSTON RD": "503",
    "505 DUNDAS": "505",
    "506 CARLTON": "506",
    "507 LONG BRANCH": "507",
    "508 LAKESHORE": "508",
    "509 HARBOURFRONT": "509",
    "509 HARBOUR FRONT": "509",
    "510 SPADINA": "510",
    "511 BATHURST": "511",
    "512 ST. CLAIR": "512",
    "512 ST CLAIR": "512",
    "514 CHERRY": "514",
}

# Recognized night-service labels
NIGHT_ALIASES = {
    "301 QUEEN": "301",
    "303 KINGSTON ROAD": "303",
    "303 KINGSTON ROAD NIGH": "303",
    "303 KINGSTON RD": "303",
    "303 KINGSTOM": "303",
    "304 KING": "304",
    "305 DUNDAS": "305",
    "306 CARLTON": "306",
    "309 HARBOURFRONT": "309",
    "310 SPADINA": "310",
    "311 BATHURST": "311",
}

def classify_route(value):
    if value == "MISSING":
        return "", "Unknown", "Needs Review", "Missing route label"

    original = str(value).strip()
    upper = original.upper()

    # RAD-related records
    if "RAD" in upper:
        return "", "RAD", "Classified", "RAD-related label"

    # Shuttle and replacement bus records
    if "SHUTTLE" in upper or "BUS" in upper:
        return "", "Shuttle", "Classified", "Shuttle or bus service"

    # Operational records
    operational_terms = [
        "OVERHEAD", "STORM", "TEST", "TRAINING",
        "CARHOUSE", "FLEET", "EXTRA", "TRACK",
        "RUN IN", "RUN-IN", "OPERATING AS",
        "PRIVATE", "VEHICLE", "OTC", "GARAGE"
    ]

    if any(term in upper for term in operational_terms):
        return "", "Operational", "Classified", "Operational label"
    
    # Recognized night-service aliases
    if upper in NIGHT_ALIASES:
        return (
            NIGHT_ALIASES[upper],
            "Night",
            "Classified",
            "Recognized night-service alias"
        )

    # Explicit night-service labels
    if "NIGHT" in upper:
        match = re.match(r"^(\d{3})", upper)
        code = match.group(1) if match else ""
        return code, "Night", "Classified", "Night-service label"

    # Normalize simple numeric labels such as 501.0
    if re.fullmatch(r"\d+(\.0)?", upper):
        code = upper.replace(".0", "")

        if code in DAY_ROUTES:
            return code, "Regular", "Classified", "Standard route number"

        if code in NIGHT_ROUTES:
            return code, "Night", "Classified", "Night route number"

        return "", "Other Numeric", "Needs Review", "Unverified numeric identifier"

    # Exact known route aliases
    if upper in ALIASES:
        return ALIASES[upper], "Regular", "Classified", "Recognized route alias"

    # Explicit route branch variants
    branch_match = re.fullmatch(
        r"(504[ABCD](?:/C)? KING|504 KING \([AB]-BRANCH\))",
        upper
    )

    if branch_match:
        return "504", "Route Variant", "Classified", "504 branch variant"

    return "", "Unknown", "Needs Review", "Requires manual review"


# Apply classification
results = routes["Original_Route"].apply(classify_route)

routes[["Route_Code", "Service_Type", "Mapping_Status", "Notes"]] = (
    pd.DataFrame(results.tolist(), index=routes.index)
)

# Preserve the original label and record count
routes.to_csv(OUTPUT_FILE, index=False)

print("\nROUTE MAPPING CREATED")
print(f"Total labels: {len(routes)}")
print(f"Saved to: {OUTPUT_FILE}")

print("\nCLASSIFICATION SUMMARY")
print(routes["Service_Type"].value_counts(dropna=False).to_string())

print("\nLABELS NEEDING REVIEW")
review = routes[routes["Mapping_Status"] == "Needs Review"]

print(f"Total requiring review: {len(review)}")
print(review.to_string(index=False))

# RECORD-LEVEL MAPPING COVERAGE

print("\nRECORD-LEVEL MAPPING COVERAGE")

coverage = (
    routes.groupby(
        ["Service_Type", "Mapping_Status"],
        dropna=False
    )["Record_Count"]
    .sum()
    .reset_index()
    .sort_values("Record_Count", ascending=False)
)

coverage["Percentage"] = (
    coverage["Record_Count"] / routes["Record_Count"].sum() * 100
)

print(coverage.to_string(index=False))

total_records = routes["Record_Count"].sum()
classified_records = routes.loc[
    routes["Mapping_Status"] == "Classified",
    "Record_Count"
].sum()

print(f"\nTotal records: {total_records:,}")
print(f"Classified records: {classified_records:,}")
print(f"Records needing review: {total_records - classified_records:,}")
print(
    f"Classification coverage: "
    f"{classified_records / total_records * 100:.2f}%"
)