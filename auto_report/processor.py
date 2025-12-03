import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_summary(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": df.isnull().sum().to_dict(),
        "describe": df.describe(include='all').to_dict()
    }

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