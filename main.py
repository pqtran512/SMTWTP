from aco import ACO
from local_search import local_search
from genetic_algorithm import ga_evolve_population
from utils import total_weighted_tardiness
from data import n_jobs, jobs
import random
import time

variants = ["aco", "aco_ls", "aco_ga"]
bestTWT = {}
runtimes = {}

for method in variants:
    print(f"\n===== Running {method.upper()} =====")
    aco = ACO(n_ants=50, iterations=50, beta=3, q0=0.9, rho=0.1)
    start_time = time.time()

    for it in range(aco.iterations):
        solutions = aco.construct_solution()

        if method == "aco_ls":
            solutions = [local_search(sol, order=('interchange', 'insert'), max_steps=100, enable=True) for sol in solutions]
        elif method == "aco_ga":
            solutions = ga_evolve_population(solutions, n_children=20, top_k=10, mutation_prob=0.2)

        best_iteration = min(solutions, key=total_weighted_tardiness)
        best_cost = total_weighted_tardiness(best_iteration)

        if best_cost < aco.best_global_cost:
            aco.best_global = best_iteration
            aco.best_global_cost = best_cost

        aco.update_pheromone(solutions, k=5)
        print(f"{method.upper()} - Iter {it+1}/{aco.iterations} | TWT = {best_cost} | Global Best = {aco.best_global_cost}")

    runtime = time.time() - start_time
    bestTWT[method] = aco.best_global_cost
    runtimes[method] = runtime

# === Add Random and Greedy Baselines ===
random_order = list(range(n_jobs))
random.shuffle(random_order)
greedy_order = sorted(range(n_jobs), key=lambda j: jobs[j][1])

print("\n==================== FINAL COMPARISON ====================")
print(f"{'Method':<25}| {'Best TWT':<12}| {'Runtime (s)'}")
print("-------------------------|-------------|--------------")
print(f"{'Random order':<25}| {total_weighted_tardiness(random_order):<12}| {'-'}")
print(f"{'Greedy (due date)':<25}| {total_weighted_tardiness(greedy_order):<12}| {'-'}")
print(f"{'ACO':<25}| {bestTWT['aco']:<12}| {runtimes['aco']:.2f}")
print(f"{'ACO + Local Search':<25}| {bestTWT['aco_ls']:<12}| {runtimes['aco_ls']:.2f}")
print(f"{'ACO + Genetic Algorithm':<25}| {bestTWT['aco_ga']:<12}| {runtimes['aco_ga']:.2f}")
print("==========================================================")
