import numpy as np
from data import jobs

def total_weighted_tardiness(order):
    time = 0
    twt = 0

    for j in order:
        pj, dj, wj = jobs[j]
        time += pj
        tardiness = max(0, time - dj)
        twt += tardiness * wj

    return twt

def calculate_heuristic(jobs):
    import numpy as np
    return np.array([1.0 / (d + 1e-6) for _, d, _ in jobs])
