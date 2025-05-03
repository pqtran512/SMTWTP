import os
import csv
import matplotlib.pyplot as plt

convergence_dir = "results/convergence"
output_dir = "results/plots"
os.makedirs(output_dir, exist_ok=True)

# Iterate over each convergence log file
for filename in os.listdir(convergence_dir):
    if filename.endswith(".csv"):
        filepath = os.path.join(convergence_dir, filename)

        with open(filepath, newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            histories = [list(map(float, row)) for row in reader]

        # Compute stats per iteration
        T = len(histories[0])
        avg_per_iter = [sum(hist[i] for hist in histories) / len(histories) for i in range(T)]
        min_per_iter = [min(hist[i] for hist in histories) for i in range(T)]
        max_per_iter = [max(hist[i] for hist in histories) for i in range(T)]

        # Plot
        plt.figure(figsize=(10, 6))
        iterations = range(1, T + 1)
        plt.plot(iterations, avg_per_iter, marker='o', label='Average')
        plt.fill_between(iterations, min_per_iter, max_per_iter, color='gray', alpha=0.3, label='Min-Max Range')

        plt.title(f"Convergence: {filename.replace('conv_', '').replace('.csv', '')}")
        plt.xlabel("Iteration")
        plt.ylabel("Best TWT")
        plt.ylim(min(min_per_iter) * 0.98, max(max_per_iter) * 1.02)  # Dynamic Y-axis range
        plt.legend()
        plt.grid(True)

        # Save plot
        save_path = os.path.join(output_dir, filename.replace(".csv", ".png"))
        plt.savefig(save_path)
        plt.close()

print(f"✅ Saved convergence plots (avg + min/max) to: {output_dir}")
