from pathlib import Path
import xml.etree.ElementTree as ET

PROJECT_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_DIR / "data" / "raw" / "reference"
    / "Code Descriptions.xml"
)

tree = ET.parse(INPUT_FILE)
root = tree.getroot()

print("\nXML ROOT")
print(root.tag)
print(root.attrib)

print("\nFIRST 10 XML ELEMENTS")

for element in list(root)[:10]:
    print("\nElement:", element.tag)
    print("Attributes:", element.attrib)

    for child in list(element):
        print(f"  {child.tag}: {child.text}")