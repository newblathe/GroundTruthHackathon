# ------------------------------------------------------------
# processor.py
# Contains all dataset analysis and visualization logic.
#
# Responsibilities:
#   1. Compute basic dataset statistics
#   2. Summarize missing values
#   3. Generate histograms for numeric columns
#   4. Compute correlation matrices
#
# This module transforms raw data into structured analytics that can be consumed by both the AI insight engine and the report generation pipeline.
# ------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Dataset Summary Generator
def generate_summary(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": df.isnull().sum().to_dict(),
        "describe": df.describe(include='all').to_dict()
    }

# Plots Generator
def generate_plots(df):
    plot_images = []
    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:
        plt.figure(figsize=(4, 3))
        df[col].hist()
        plt.title(f"Distribution of {col}")

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)

        plot_images.append((col, buf))
        plt.close()

    return plot_images

# Heatmap Generator

def generate_corr_heatmap(df):
    num_df = df.select_dtypes(include="number")
    if num_df.empty:
        return None

    plt.figure(figsize=(5, 3))
    sns.heatmap(num_df.corr(), annot=True, cmap="Blues")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close()
    return buf