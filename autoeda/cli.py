import sys
import pandas as pd
from .eda import autoeda

def main():
    if len(sys.argv) < 2:
        print("usage: autoeda <csv_file>")
        sys.exit(1)

    csv_path = sys.argv[1]

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"failed to load file: {e}")
        sys.exit(1)

    a = autoeda(df)
    report = a.analyze()
    output = "autoeda_report.html"
    a.save_html(output)

    print(f"report saved: {output}")
