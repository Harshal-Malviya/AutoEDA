import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import io
import base64

def _fig_to_base64(fig):
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=90, bbox_inches="tight")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return b64

def plot_distribution_base64(df, col):
    ser = df[col].dropna()

    # consistent figure size for all plots
    fig, ax = plt.subplots(figsize=(4, 2.6))

    if pd.api.types.is_numeric_dtype(ser):
        ax.hist(ser, bins=25, color="#3b82f6", edgecolor="white")
    else:
        vc = ser.nlargest(6)
        ax.bar(vc.index.astype(str), vc.values, color="#3b82f6")
        ax.set_xticklabels(vc.index.astype(str), rotation=45, ha="right", fontsize=7)

    ax.set_title(f"{col}", fontsize=10)
    return _fig_to_base64(fig)

def plot_correlation_base64(df):
    corr = df.corr()

    fig, ax = plt.subplots(figsize=(4.5, 4.2))
    cax = ax.matshow(corr, cmap="coolwarm")

    fig.colorbar(cax)

    ticks = np.arange(len(corr.columns))
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(corr.columns, rotation=90, fontsize=7)
    ax.set_yticklabels(corr.columns, fontsize=7)

    ax.set_title("correlation matrix", pad=20, fontsize=11)

    # annotate each cell
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            val = corr.iloc[i, j]
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    color="white" if abs(val) > 0.5 else "black",
                    fontsize=7)

    return _fig_to_base64(fig)

def plot_box_base64(df, col):
    ser = df[col].dropna()

    fig, ax = plt.subplots(figsize=(3.5, 2.8))
    ax.boxplot(ser, vert=True, patch_artist=True,
               boxprops=dict(facecolor="#3b82f6", alpha=0.6))
    
    ax.set_title(f"{col}", fontsize=10)
    ax.set_xticks([])

    return _fig_to_base64(fig)

def plot_scatter_base64(df, x, y):
    fig, ax = plt.subplots(figsize=(4, 2.6))
    ax.scatter(df[x], df[y], alpha=0.6, s=12, color="#3b82f6")
    ax.set_xlabel(x, fontsize=8)
    ax.set_ylabel(y, fontsize=8)
    ax.set_title(f"{x} vs {y}", fontsize=10)
    return _fig_to_base64(fig)
