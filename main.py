from aco import ACO
from local_search import local_search
from utils import total_weighted_tardiness
from data import n_jobs

aco = ACO(n_ants=30, iterations=500, beta=3, q0=0.9, evaporation=0.3)

for it in range(aco.iterations):
    solutions = aco.construct_solution()

    improved = [local_search(sol) for sol in solutions]

    best_iteration = min(improved, key=total_weighted_tardiness)
    
    best_cost = total_weighted_tardiness(best_iteration)

    if best_cost < aco.best_global_cost:
        aco.best_global = best_iteration
        aco.best_global_cost = best_cost

    aco.update_pheromone(best_iteration)
    # print(f'Iter {it+1}: Best Cost = {best_cost}')

print('n_jobs:', n_jobs)
print('n_ants:', aco.n_ants)
print('iterations:', aco.iterations)
print('beta:', aco.beta)
print('q0:', aco.q0)
print('evaporation:', aco.evaporation)
print('Best order :', aco.best_global)
print('Total Weighted Tardiness:', aco.best_global_cost)
