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

def calculate_heuristic(n_jobs):
    import numpy as np

    heuristic = np.zeros((n_jobs, n_jobs))
    for i in range(n_jobs):
        for j in range(n_jobs):
            if i != j:
                heuristic[i][j] = 1 / (jobs[j][1] + 1e-6)
    return heuristic
