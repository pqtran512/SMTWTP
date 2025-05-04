import random
from utils import total_weighted_tardiness

def local_search(solution, order=('interchange', 'insert'), max_steps=100, enable=True):
    current = solution[:]
    if enable:
        for method in order:
            if method == 'interchange':
                current = local_search_interchange(current, max_steps)
            elif method == 'insert':
                current = local_search_insert(current, max_steps)
    return current

def local_search_interchange(solution, max_steps=100):
    best = solution[:]
    best_cost = total_weighted_tardiness(best)
    n = len(solution)
    steps = 0

    while steps < max_steps:
        improved = False
        indices = list(range(n))
        random.shuffle(indices)

        for i in indices:
            for j in indices:
                if i >= j:
                    continue
                candidate = best[:]
                candidate[i], candidate[j] = candidate[j], candidate[i]
                cost = total_weighted_tardiness(candidate)
                steps += 1
                if cost < best_cost:
                    best = candidate
                    best_cost = cost
                    improved = True
                    break
            if improved or steps >= max_steps:
                break
        if not improved:
            break

    return best

def local_search_insert(solution, max_steps=100):
    best = solution[:]
    best_cost = total_weighted_tardiness(best)
    n = len(solution)
    steps = 0

    while steps < max_steps:
        improved = False
        indices = list(range(n))
        random.shuffle(indices)

        for i in indices:
            for j in indices:
                if i == j:
                    continue
                candidate = best[:]
                job = candidate.pop(i)
                candidate.insert(j, job)
                cost = total_weighted_tardiness(candidate)
                steps += 1
                if cost < best_cost:
                    best = candidate
                    best_cost = cost
                    improved = True
                    break
            if improved or steps >= max_steps:
                break
        if not improved:
            break

    return best
