from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
FILE = PROJECT_DIR / "output" / "route_label_frequency.csv"

routes = pd.read_csv(FILE)

print("\nFINAL ROUTE LABELS 321–362")
print(
    routes.iloc[320:362].to_string(index=False)
)