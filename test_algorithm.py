from aco import ACO
from local_search import local_search
from simulated_annealing import simulated_annealing
from utils import total_weighted_tardiness
from data import n_jobs, jobs
import random
import time
import os
import csv
import statistics
from tqdm import tqdm

variants = ["aco", "aco_ls", "aco_sa"]
bestTWT = {}
avgTWT = {}
stdTWT = {}
runtimes = {}
n_runs = 10

os.makedirs("results", exist_ok=True)
test_algorithm_file = "results/test_algorithm.csv"

# prepare result log header
with open(test_algorithm_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["method", "run", "best_twt", "runtime"])

for method in variants:
    print(f"\n===== Running {method.upper()} for {n_runs} runs =====")
    best = float("inf")
    total_time = 0
    twt_runs = []

    for run in range(n_runs):
        print(f"\n--- {method.upper()} Run {run+1}/{n_runs} ---")
        aco = ACO(n_ants=50, iterations=50, beta=3, q0=0.9, rho=0.1)
        start_time = time.time()

        with tqdm(total=aco.iterations, desc=f"{method.upper()} Run {run+1}", leave=False) as pbar:
            for it in range(aco.iterations):
                solutions = aco.construct_solution()

                if method == "aco_ls":
                    solutions = [local_search(sol, order=('interchange', 'insert'), max_steps=100, enable=True) for sol in solutions]
                if method == "aco_sa":
                    solutions = [simulated_annealing(s, max_iter=50) for s in solutions]

                best_iteration = min(solutions, key=total_weighted_tardiness)
                best_cost = total_weighted_tardiness(best_iteration)

                if best_cost < aco.best_global_cost:
                    aco.best_global = best_iteration
                    aco.best_global_cost = best_cost

                aco.update_pheromone(solutions, k=5)
                pbar.set_postfix(TWT=best_cost, Global=aco.best_global_cost)
                pbar.update(1)

        runtime = time.time() - start_time
        best = min(best, aco.best_global_cost)
        total_time += runtime
        twt_runs.append(aco.best_global_cost)

        # append summary result to CSV
        with open(test_algorithm_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([method, run + 1, aco.best_global_cost, round(runtime, 2)])

        print(f"✅ Done {method.upper()} Run {run+1} Finished → TWT = {aco.best_global_cost:.0f}, Time = {runtime:.2f}s")

    avg_twt = sum(twt_runs) / n_runs
    std_twt = statistics.stdev(twt_runs) if n_runs > 1 else 0

    bestTWT[method] = best
    avgTWT[method] = avg_twt
    stdTWT[method] = std_twt
    runtimes[method] = total_time / n_runs

# === Add Random and Greedy Baselines ===
random_order = list(range(n_jobs))
random.shuffle(random_order)
greedy_order = sorted(range(n_jobs), key=lambda j: jobs[j][1])

print("\n==================== FINAL COMPARISON ====================")
print(f"{'Method':<30}| {'Best TWT':<12}| {'Avg TWT':<12}| {'Std TWT':<10}| {'Avg Runtime (s)'}")
print("------------------------------|-------------|-------------|------------|------------------")
print(f"{'Random order':<30}| {total_weighted_tardiness(random_order):<12}| {'-':<12}| {'-':<10}| {'-'}")
print(f"{'Greedy (due date)':<30}| {total_weighted_tardiness(greedy_order):<12}| {'-':<12}| {'-':<10}| {'-'}")
print(f"{'ACO':<30}| {bestTWT['aco']:<12}| {avgTWT['aco']:<12.2f}| {stdTWT['aco']:<10.2f}| {runtimes['aco']:.2f}")
print(f"{'ACO + Local Search':<30}| {bestTWT['aco_ls']:<12}| {avgTWT['aco_ls']:<12.2f}| {stdTWT['aco_ls']:<10.2f}| {runtimes['aco_ls']:.2f}")
print(f"{'ACO + Simulated Annealing':<30}| {bestTWT['aco_sa']:<12}| {avgTWT['aco_sa']:<12.2f}| {stdTWT['aco_sa']:<10.2f}| {runtimes['aco_sa']:.2f}")
print("==========================================================")
