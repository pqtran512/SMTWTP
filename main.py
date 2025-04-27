from aco import ACO
# from local_search import local_search
from utils import total_weighted_tardiness

aco = ACO(n_ants=10, iterations=50)

for it in range(aco.iterations):
    solutions = aco.construct_solution()

    best_iteration = min(solutions, key=total_weighted_tardiness)
    
    best_cost = total_weighted_tardiness(best_iteration)

    if best_cost < aco.best_global_cost:
        aco.best_global = best_iteration
        aco.best_global_cost = best_cost

    aco.update_pheromone(best_iteration)
    print(f'Iter {it+1}: Best Cost = {best_cost}')

print('Best order :', aco.best_global)
print('Total Weighted Tardiness:', aco.best_global_cost)
