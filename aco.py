import random
import numpy as np
from data import n_jobs, jobs
from utils import calculate_heuristic, total_weighted_tardiness

class ACO:
    def __init__(self, n_ants=20, iterations=100, beta=3, q0=0.9, evaporation=0.1):
        self.n_ants = n_ants
        self.iterations = iterations
        self.beta = beta
        self.q0 = q0
        self.evaporation = evaporation
        self.pheromone = np.ones((n_jobs, n_jobs))
        self.heuristic = calculate_heuristic(n_jobs)
        self.best_global = None
        self.best_global_cost = float('inf')

    def construct_solution(self):
        solutions = []
        
        for _ in range(self.n_ants):
            visited = []

            # chọn ngẫu nhiên 1 job để bắt đầu
            current = random.randint(0, n_jobs - 1)
            visited.append(current)

            while len(visited) < n_jobs:
                candidates = [j for j in range(n_jobs) if j not in visited]

                # tính xác suất chọn job kế tiếp
                if random.random() < self.q0:
                    next_job = max(candidates, key=lambda j: self.pheromone[current][j] * self.heuristic[current][j]**self.beta)
                else:
                    probs = [self.pheromone[current][j] * self.heuristic[current][j]**self.beta for j in candidates]
                    total = sum(probs)
                    probs = [p / total for p in probs]
                    next_job = random.choices(candidates, weights=probs)[0]

                visited.append(next_job)
                current = next_job

            solutions.append(visited)
            
        return solutions

    def update_pheromone(self, best_solution):
        self.pheromone *= (1 - self.evaporation)

        cost = total_weighted_tardiness(best_solution)
        if cost == 0:
            cost = 1e-6  # tránh chia cho 0

        for i in range(n_jobs - 1):
            a = best_solution[i]
            b = best_solution[i + 1]
            self.pheromone[a][b] += 1.0 / cost