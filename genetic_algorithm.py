import random
from utils import total_weighted_tardiness

# -----------------------------
# PMX Crossover
# -----------------------------
def pmx_crossover(parent1, parent2):
    size = len(parent1)
    child = [None] * size

    # Chọn 2 điểm cắt
    cx1, cx2 = sorted(random.sample(range(size), 2))

    # Copy đoạn giữa từ cha 1
    child[cx1:cx2 + 1] = parent1[cx1:cx2 + 1]

    # Ánh xạ các gene trong đoạn đó từ cha 2
    for i in range(cx1, cx2 + 1):
        if parent2[i] not in child:
            val = parent2[i]
            pos = i
            while True:
                mapped_val = parent1[pos]
                pos = parent2.index(mapped_val)
                if child[pos] is None:
                    child[pos] = val
                    break

    # Điền phần còn lại từ cha 2
    for i in range(size):
        if child[i] is None:
            child[i] = parent2[i]

    return child

# -----------------------------
# Đột biến: Swap 2 vị trí
# -----------------------------
def mutate(solution, mutation_prob=0.2):
    if random.random() < mutation_prob:
        i, j = random.sample(range(len(solution)), 2)
        solution[i], solution[j] = solution[j], solution[i]
    return solution

# -----------------------------
# GA tiến hóa 1 thế hệ
# -----------------------------
def ga_evolve_population(population, n_children=20, top_k=10, mutation_prob=0.2):
    # Chọn top-k lời giải tốt nhất để lai
    ranked = sorted(population, key=total_weighted_tardiness)
    parents_pool = ranked[:top_k]

    children = []
    while len(children) < n_children:
        p1, p2 = random.sample(parents_pool, 2)
        child = pmx_crossover(p1, p2)
        child = mutate(child, mutation_prob)
        children.append(child)

    # Trả về top lời giải tốt nhất từ con
    all_candidates = ranked + children
    next_generation = sorted(all_candidates, key=total_weighted_tardiness)[:len(population)]
    return next_generation
