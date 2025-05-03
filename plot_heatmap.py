import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load result CSV
csv_path = "results/grid_results.csv"
df = pd.read_csv(csv_path)

# Filter only ACO (exclude LS and GA)
df_aco = df[df["method"] == "aco"]

# Create output folder
output_dir = "results/heatmaps"
os.makedirs(output_dir, exist_ok=True)

# Define heatmap plots to generate: (row, col, value)
heatmap_configs = [
    ("m", "q0", "avg_twt"),
    ("m", "T", "avg_twt"),
    ("beta", "rho", "avg_twt"),
    ("m", "q0", "runtime"),
]

for row, col, value in heatmap_configs:
    pivot_table = df_aco.pivot_table(index=row, columns=col, values=value)

    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap="viridis")
    plt.title(f"Heatmap of {value} by {row} and {col}")
    plt.ylabel(row)
    plt.xlabel(col)

    filename = f"heatmap_{value}_{row}_vs_{col}.png"
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

print(f"✅ Heatmaps saved to: {output_dir}")
