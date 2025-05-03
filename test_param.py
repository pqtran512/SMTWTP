import time
import csv
import random
import os
from itertools import product
from tqdm import tqdm
from aco import ACO
from genetic_algorithm import ga_evolve_population
from local_search import local_search
from utils import total_weighted_tardiness
from data import n_jobs, jobs

# ==== PARAMETER GRID (only ACO) ====
param_grid = {
    "m": [10, 25, 50],
    "T": [30, 50],
    "q0": [0.5, 0.7, 0.9],
    "beta": [1, 3],
    "rho": [0.1, 0.3],
    "method": ["aco"]
}

# ==== OUTPUTS ====
os.makedirs("results/convergence", exist_ok=True)
output_file = "results/grid_results.csv"
convergence_log_dir = "results/convergence"

header = ["m", "T", "q0", "beta", "rho", "method", "best_twt", "avg_twt", "runtime"]
results = []
combinations = list(product(param_grid['m'], param_grid['T'], param_grid['q0'], param_grid['beta'], param_grid['rho'], param_grid['method']))

total_combinations = len(combinations)
best_config = None
best_global_twt = float("inf")

for idx, (m, T, q0, beta, rho, method) in enumerate(combinations, 1):
    print(f"\nRunning {idx}/{total_combinations}: m={m}, T={T}, q0={q0}, beta={beta}, rho={rho}, method={method}")

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
    results.append([m, T, q0, beta, rho, method, best_twt, avg_twt, round(runtime, 2)])

    # Save convergence log
    log_file = os.path.join(convergence_log_dir, f"conv_m{m}_T{T}_q{q0}_b{beta}_r{rho}.csv")
    with open(log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([f"iter{i+1}" for i in range(T)])
        writer.writerows(all_histories)

    if best_twt < best_global_twt:
        best_global_twt = best_twt
        best_config = (m, T, q0, beta, rho)

    print(f"✅ Done {idx}/{total_combinations} → Best TWT = {best_twt}, Avg TWT = {avg_twt:.2f}, Time = {runtime:.2f}s")

# ==== Run ACO+LS and ACO+GA using best ACO config ====
best_m, best_T, best_q0, best_beta, best_rho = best_config

for method in ["aco_ls", "aco_ga"]:
    print(f"\n🔁 Running {method} with best ACO config: m={best_m}, T={best_T}, q0={best_q0}, beta={best_beta}, rho={best_rho}")
    best_twt = float("inf")
    total_twt = 0
    n_runs = 3
    start_time = time.time()

    with tqdm(total=n_runs * best_T, desc=f"{method}", unit="iter", leave=False) as pbar:
        for _ in range(n_runs):
            aco = ACO(n_ants=best_m, iterations=best_T, beta=best_beta, q0=best_q0, rho=best_rho)
            for t in range(best_T):
                solutions = aco.construct_solution()
                if method == "aco_ls":
                    solutions = [local_search(s, order=("interchange", "insert"), max_steps=100, enable=True) for s in solutions]
                else:
                    solutions = ga_evolve_population(solutions, n_children=10, top_k=10, mutation_prob=0.2)

                best_iter = min(solutions, key=total_weighted_tardiness)
                cost = total_weighted_tardiness(best_iter)
                if cost < aco.best_global_cost:
                    aco.best_global = best_iter
                    aco.best_global_cost = cost
                aco.update_pheromone(solutions, k=5)
                pbar.update(1)

            best_twt = min(best_twt, aco.best_global_cost)
            total_twt += aco.best_global_cost

    avg_twt = total_twt / n_runs
    runtime = time.time() - start_time
    results.append([best_m, best_T, best_q0, best_beta, best_rho, method, best_twt, avg_twt, round(runtime, 2)])
    print(f"✅ {method} done → Best TWT = {best_twt}, Avg TWT = {avg_twt:.2f}, Time = {runtime:.2f}s")

# ==== Add Random and Greedy for comparison ====
random_order = list(range(n_jobs))
random.shuffle(random_order)
random_twt = total_weighted_tardiness(random_order)

jobs_sorted_by_due = sorted(range(n_jobs), key=lambda j: jobs[j][1])
greedy_twt = total_weighted_tardiness(jobs_sorted_by_due)

results.append(["random", "-", "-", "-", "-", "random", random_twt, random_twt, 0])
results.append(["greedy", "-", "-", "-", "-", "greedy", greedy_twt, greedy_twt, 0])

# ==== WRITE CSV ====
os.makedirs("results", exist_ok=True)
with open(output_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(results)

print("\n✅ All parameter combinations completed. Results saved to", output_file)
