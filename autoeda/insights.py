import pandas as pd
import numpy as np

def missing_summary(df):
    res = {}
    for col in df.columns:
        total = len(df)
        n_miss = int(df[col].isna().sum())
        percent = float(n_miss) / total * 100 if total else 0.0
        res[col] = {"n_missing": n_miss, "percent_missing": percent}
    return res

def dtype_summary(df):
    res = {}
    for col in df.columns:
        ser = df[col]
        dtype = str(ser.dtype)
        nunique = ser.nunique(dropna=True)
        total = ser.shape[0]
        unique_ratio = float(nunique) / total if total else 0.0
        res[col] = {"dtype": dtype, "n_unique": int(nunique), "unique_ratio": unique_ratio}
    return res

def outlier_summary(df):
    res = {}
    for col in df.select_dtypes(include=["number"]).columns:
        ser = df[col].dropna()
        if ser.empty:
            res[col] = {"n_outliers": 0}
            continue
        q1 = ser.quantile(0.25)
        q3 = ser.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        n_out = int(((ser < lower) | (ser > upper)).sum())
        res[col] = {"n_outliers": n_out, "iqr": float(iqr)}
    return res