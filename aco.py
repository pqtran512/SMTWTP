import random
import numpy as np
from data import n_jobs, jobs
from utils import calculate_heuristic, total_weighted_tardiness

class ACO:
    def __init__(self, n_ants=20, iterations=100, beta=3, q0=0.9, evaporation=0.1, tau_min=1e-6, tau_max=5.0):
        self.n_ants = n_ants
        self.iterations = iterations
        self.beta = beta
        self.q0 = q0
        self.evaporation = evaporation
        self.tau_min = tau_min
        self.tau_max = tau_max
        self.pheromone = np.ones((n_jobs, n_jobs))
        self.heuristic = calculate_heuristic(jobs)  # MDD heuristic
        self.best_global = None
        self.best_global_cost = float('inf')

    def construct_solution(self):
        solutions = []
        tau_0 = 1.0
        xi = 0.1  # online pheromone decay rate

        for _ in range(self.n_ants):
            visited = set()
            solution = []

            for pos in range(n_jobs):
                candidates = [j for j in range(n_jobs) if j not in visited]
                if random.random() < self.q0:
                    # Exploitation
                    next_job = max(candidates, key=lambda j: self.pheromone[pos][j] * (self.heuristic[j] ** self.beta))
                else:
                    # Exploration
                    probs = [self.pheromone[pos][j] * (self.heuristic[j] ** self.beta) for j in candidates]
                    total = sum(probs)
                    probs = [p / total for p in probs]
                    next_job = random.choices(candidates, weights=probs)[0]

                solution.append(next_job)
                visited.add(next_job)

                # Online pheromone update
                self.pheromone[pos][next_job] = (1 - xi) * self.pheromone[pos][next_job] + xi * tau_0

            solutions.append(solution)

        return solutions

    def update_pheromone(self, solutions, k=5):
        self.pheromone *= (1 - self.evaporation)

        # cập nhật pheromone từ top-k solutions 
        top_k = sorted(solutions, key=total_weighted_tardiness)[:k]
        for sol in top_k:
            cost = total_weighted_tardiness(sol)
            if cost == 0:
                cost = 1e-6  # tránh chia cho 0
            for pos, job in enumerate(sol):
                self.pheromone[pos][job] += 1.0 / cost

        # dynamic pheromone bounds
        self.tau_max = 1.0 / ((1 - self.evaporation) * self.best_global_cost)
        self.pheromone = np.clip(self.pheromone, self.tau_min, self.tau_max)
