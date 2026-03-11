import os
import io
import base64
import pandas as pd
from streamlit import html, title
from tqdm import tqdm
from .visualizations import (
    plot_distribution_base64,
    plot_correlation_base64,
    plot_box_base64,
    plot_scatter_base64
)
from .insights import missing_summary, dtype_summary, outlier_summary
from .utils import render_html_report

def _is_notebook():
    try:
        from IPython import get_ipython
        if "IPKernelApp" not in get_ipython().config:
            return False
    except:
        return False
    return True

class autoeda:
    def __init__(self, df):
        self.df = df.copy()
        self.report = {
            "meta": {},
            "missing": {},
            "dtypes": {},
            "distributions": {},
            "correlations": None,
            "outliers": {},
            "insights": [],
            "spread": {},
            "boxplots": {},
            "scatterplots": {}
        }

    def analyze(self, sample_threshold=200000):
        total_cells = self.df.size
        missing_cells = self.df.isna().sum().sum()

        self.report["summary"] = {
            "rows": int(self.df.shape[0]),
            "columns": int(self.df.shape[1]),
            "missing_percent": round((missing_cells / total_cells) * 100, 2),
            "duplicates": int(self.df.duplicated().sum()),
            "memory": round(self.df.memory_usage(deep=True).sum() / (1024**2), 2)
        }
    
        self.report["missing"] = missing_summary(self.df)
        self.report["dtypes"] = dtype_summary(self.df)

        numeric_cols = self.df.select_dtypes(include=["number"]).columns.tolist()

        # distributions
        for col in tqdm(self.df.columns, desc="generating distributions"):
            try:
                b64 = plot_distribution_base64(self.df, col)
                self.report["distributions"][col] = b64
            except Exception:
                continue

        # correlations
        if len(numeric_cols) >= 2:
            self.report["correlations"] = plot_correlation_base64(self.df[numeric_cols])

        # outliers
        self.report["outliers"] = outlier_summary(self.df)

        # spread summary
        for col in tqdm(numeric_cols, desc="calculating spread"):
            ser = self.df[col].dropna()
            self.report["spread"][col] = {
                "min": float(ser.min()),
                "max": float(ser.max()),
                "mean": float(ser.mean()),
                "std": float(ser.std()),
                "p25": float(ser.quantile(0.25)),
                "p50": float(ser.quantile(0.50)),
                "p75": float(ser.quantile(0.75))
            }

        # boxplots
        for col in tqdm(numeric_cols, desc="generating boxplots"):
            try:
                b64_box = plot_box_base64(self.df, col)
                self.report["boxplots"][col] = b64_box
            except Exception:
                continue

        # scatterplots: top 20 correlated numeric pairs
        self.report["scatterplots"] = {}
        if len(numeric_cols) >= 2:
            corr = self.df[numeric_cols].corr().abs()
            pairs = []

            for i in range(len(numeric_cols)):
                for j in range(i + 1, len(numeric_cols)):
                    pairs.append((numeric_cols[i], numeric_cols[j], corr.iloc[i, j]))

            # top 20 correlated pairs
            pairs = sorted(pairs, key=lambda x: x[2], reverse=True)[:20]

            for x, y, _ in tqdm(pairs, desc="generating scatterplots"):
                try:
                    b64_scat = plot_scatter_base64(self.df, x, y)
                    self.report["scatterplots"][f"{x}_vs_{y}"] = b64_scat
                except Exception:
                    continue

        # insights
        self.report["insights"] = self._generate_insights()

        return self.report

    def _generate_insights(self):
        ins = []
        for col, info in self.report["missing"].items():
            if info["percent_missing"] > 30:
                ins.append(f"column '{col}' has >30% missing values")
        for col, dt in self.report["dtypes"].items():
            if dt["dtype"] == "object" and dt["unique_ratio"] < 0.05:
                ins.append(f"column '{col}' is likely categorical")
        for col, out in self.report["outliers"].items():
            if out.get("n_outliers", 0) > 0:
                ins.append(f"column '{col}' has potential outliers (count={out.get('n_outliers')})")
        return ins

    def save_html(self, filepath="autoeda_report.html", title="AutoEDA Report"):
        html = render_html_report(self.report, title=title)

        if _is_notebook():
            try:
                from IPython.display import display, HTML
                display(HTML(html))
                return
            except:
                pass

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        return filepath
    
    def show(self, title="AutoEDA Report"):
        html = render_html_report(self.report, title=title)

        try:
            from IPython.display import display, HTML
            display(HTML(html))
        except ImportError:
            print("not running in a notebook environment")