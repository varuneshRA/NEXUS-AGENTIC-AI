import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../../generated_plots"))

os.makedirs(OUTPUT_DIR, exist_ok=True)

SUPPORTED_CHART_TYPES = {"bar", "line", "pie", "scatter", "heatmap"}


def generate_visual(data: list, chart_type: str, x: str, y: str = None, title: str = None, hue: str = None) -> dict:
    """Generates a chart from data and saves it to disk. Returns the file path."""
    if not data:
        return {"status": "error", "message": "No data provided for visualization."}

    if chart_type not in SUPPORTED_CHART_TYPES:
        return {
            "status": "error",
            "message": f"Unsupported chart type '{chart_type}'. Supported: {sorted(SUPPORTED_CHART_TYPES)}",
        }

    df = pd.DataFrame(data)

    if x not in df.columns:
        return {"status": "error", "message": f"Column '{x}' not found in data. Available: {list(df.columns)}"}

    if y and y not in df.columns:
        return {"status": "error", "message": f"Column '{y}' not found in data. Available: {list(df.columns)}"}

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    sns.set_theme(style="whitegrid", palette="viridis")
    fig, ax = plt.subplots(figsize=(11, 6))

    try:
        if chart_type == "bar":
            sns.barplot(data=df, x=x, y=y, hue=hue, ax=ax, errorbar=None)
        elif chart_type == "line":
            sns.lineplot(data=df, x=x, y=y, hue=hue, marker="o", ax=ax)
        elif chart_type == "pie":
            pie_data = df.groupby(x)[y].sum() if y else df[x].value_counts()
            pie_data.plot.pie(autopct="%1.1f%%", ax=ax, startangle=140)
            ax.set_ylabel("")
        elif chart_type == "scatter":
            sns.scatterplot(data=df, x=x, y=y, hue=hue, s=100, alpha=0.8, ax=ax)
        elif chart_type == "heatmap":
            pivot = df.pivot(index=x, columns=hue, values=y)
            sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)

        plt.title(title or f"{chart_type.capitalize()} Chart", fontsize=15, pad=20, fontweight="bold")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nexus_{chart_type}_{timestamp}.png"
        filepath = os.path.normpath(os.path.join(OUTPUT_DIR, filename))

        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close(fig)

        return {
            "status": "success",
            "chart_details": {
                "type": chart_type,
                "file_name": filename,
                "file_path": filepath,
                "saved_at": OUTPUT_DIR,
            },
        }
    except Exception as e:
        if "fig" in locals():
            plt.close(fig)
        return {"status": "error", "message": f"Plotting failed: {str(e)}"}
