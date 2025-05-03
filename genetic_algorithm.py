import random
from utils import total_weighted_tardiness

def crossover_ox(p1, p2):
    size = len(p1)
    a, b = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[a:b+1] = p1[a:b+1]
    fill = [j for j in p2 if j not in child]
    idx = 0
    for i in range(size):
        if child[i] is None:
            child[i] = fill[idx]
            idx += 1
    return child

def mutate_swap(ind, prob=0.2):
    if random.random() < prob:
        i, j = random.sample(range(len(ind)), 2)
        ind[i], ind[j] = ind[j], ind[i]
    return ind

def ga_evolve_population(population, n_children=10, top_k=10, mutation_prob=0.2):
    top = sorted(population, key=total_weighted_tardiness)[:top_k]
    children = []
    while len(children) < n_children:
        p1, p2 = random.sample(top, 2)
        child = crossover_ox(p1, p2)
        child = mutate_swap(child, prob=mutation_prob)
        children.append(child)
    return children
