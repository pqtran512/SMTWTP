import random
from utils import total_weighted_tardiness

def local_search(solution):
    # Tạo bản sao list solution
    best = solution[:] 

    best_cost = total_weighted_tardiness(best)

    for _ in range(5):
        i, j = random.sample(range(len(solution)), 2)
        new = best[:]

        # Hoán đổi 2 job tại i, j
        new[i], new[j] = new[j], new[i]
        cost = total_weighted_tardiness(new)
        
        if cost < best_cost:
            best = new
            best_cost = cost

    return best
