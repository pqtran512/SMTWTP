from aco import ACO
from local_search import local_search
from utils import total_weighted_tardiness
from data import n_jobs, jobs

bestTWT = []

for enable_ls in [False, True]:
    aco = ACO(n_ants=50, iterations=50, beta=3, q0=0.9, rho=0.1)
    if enable_ls:
        with_ls = "ACO with Local Seach - "
    else:
        with_ls = "Only ACO - "
    for it in range(aco.iterations):
        solutions = aco.construct_solution()

        improved = [local_search(sol, order=('interchange', 'insert'), max_steps=100, enable=enable_ls) for sol in solutions]

        best_iteration = min(improved, key=total_weighted_tardiness)
        best_cost = total_weighted_tardiness(best_iteration)

        if best_cost < aco.best_global_cost:
            aco.best_global = best_iteration
            aco.best_global_cost = best_cost

        aco.update_pheromone(improved, k=5)
        print(with_ls + f'Iter {it+1}/{aco.iterations} | TWT = {best_cost} | Global Best = {aco.best_global_cost}')
    bestTWT.append(aco.best_global_cost)

########################################################################
import random

random_order = list(range(n_jobs))
random.shuffle(random_order)
greedy_order = sorted(range(n_jobs), key=lambda j: jobs[j][1])

print(f"\n\
==================== FINAL COMPARISON ====================\n\
Method                  | Best TWT\n\
------------------------|----------------\n\
Random order            | {total_weighted_tardiness(random_order)}\n\
Greedy (due date)       | {total_weighted_tardiness(greedy_order)}\n\
ACO                     | {bestTWT[0]}\n\
ACO + Local Search      | {bestTWT[1]}\n\
===========================================================\n\
")