import time
import csv
import os
from itertools import product
from tqdm import tqdm
from aco import ACO
from utils import total_weighted_tardiness

# ==== PARAMETER GRID (only ACO) ====
param_grid = {
    "m": [10, 25, 50],
    "T": [30, 50],
    "q0": [0.5, 0.7, 0.9],
    "beta": [1, 3],
    "rho": [0.1, 0.3]
}

# ==== OUTPUTS ====
os.makedirs("results/convergence", exist_ok=True)
output_file = "results/test_param.csv"
convergence_log_dir = "results/convergence"

header = ["m", "T", "q0", "beta", "rho", "best_twt", "avg_twt", "runtime"]
results = []
combinations = list(product(param_grid['m'], param_grid['T'], param_grid['q0'], param_grid['beta'], param_grid['rho']))

total_combinations = len(combinations)

for idx, (m, T, q0, beta, rho) in enumerate(combinations, 1):
    print(f"\nRunning {idx}/{total_combinations}: m={m}, T={T}, q0={q0}, beta={beta}, rho={rho}")

    best_twt = float("inf")
    total_twt = 0
    n_runs = 3
    start_time = time.time()

    all_histories = []
    with tqdm(total=n_runs * T, desc=f"Config {idx}/{total_combinations}", unit="iter", leave=False) as pbar:
        for run in range(n_runs):
            aco = ACO(n_ants=m, iterations=T, beta=beta, q0=q0, rho=rho)
            history = []

            for t in range(T):
                solutions = aco.construct_solution()
                best_iter = min(solutions, key=total_weighted_tardiness)
                cost = total_weighted_tardiness(best_iter)
                if cost < aco.best_global_cost:
                    aco.best_global = best_iter
                    aco.best_global_cost = cost

                history.append(aco.best_global_cost)
                aco.update_pheromone(solutions, k=5)
                pbar.update(1)

            all_histories.append(history)
            best_twt = min(best_twt, aco.best_global_cost)
            total_twt += aco.best_global_cost

    avg_twt = total_twt / n_runs
    runtime = time.time() - start_time
    results.append([m, T, q0, beta, rho, best_twt, avg_twt, round(runtime, 2)])

    # Save convergence log
    log_file = os.path.join(convergence_log_dir, f"conv_m{m}_T{T}_q{q0}_b{beta}_r{rho}.csv")
    with open(log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([f"iter{i+1}" for i in range(T)])
        writer.writerows(all_histories)

    print(f"✅ Done {idx}/{total_combinations} → Best TWT = {best_twt}, Avg TWT = {avg_twt:.2f}, Time = {runtime:.2f}s")

# ==== WRITE CSV ====
with open(output_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(results)

print("\n✅ All parameter combinations completed. Results saved to", output_file)
