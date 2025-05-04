import math
import random
from utils import total_weighted_tardiness

def simulated_annealing(solution, max_iter=100, T_start=100.0, T_end=1.0, alpha=0.95):
    """
    Áp dụng simulated annealing để cải thiện hoán vị lời giải.

    Parameters:
        solution (list): Hoán vị ban đầu.
        max_iter (int): Số lần lặp tối đa.
        T_start (float): Nhiệt độ khởi đầu.
        T_end (float): Nhiệt độ kết thúc.
        alpha (float): Hệ số làm nguội.

    Returns:
        list: Lời giải cải thiện (hoặc không).
    """
    current = solution[:]
    best = current[:]
    best_cost = total_weighted_tardiness(current)
    current_cost = best_cost

    T = T_start
    iteration = 0

    while T > T_end and iteration < max_iter:
        # Hoán đổi 2 vị trí ngẫu nhiên
        i, j = sorted(random.sample(range(len(current)), 2))
        neighbor = current[:]
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

        neighbor_cost = total_weighted_tardiness(neighbor)
        delta = neighbor_cost - current_cost

        # Chấp nhận nếu tốt hơn, hoặc với xác suất nếu tệ hơn
        if delta < 0 or random.random() < math.exp(-delta / T):
            current = neighbor[:]
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best = current[:]
                best_cost = current_cost

        # Làm nguội
        T *= alpha
        iteration += 1

    return best
