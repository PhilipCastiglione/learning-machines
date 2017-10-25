"""TODO comment and properly document functions
"""

from problems.titanic import Titanic
import random

# from input, with defaults
hyperparameters = {
    'generations': 50,
    'population_size': 100,
    'factor_random_min': 0.5,
    'factor_random_max': 1.5,
    'breeding_rate': 0.2,
    'crossover_rate': 0.96,
    'mutation_rate': 0.08,
    'mutation_range': 0.1,
}

"""Print a chromosome to the console for debugging.
"""
def print_chromosome(chromosome):
    for feature in chromosome:
        line = ''
        for category in feature:
            line += "{:.2f} ".format(category)
        print(line)

"""TODO comment
"""
def select_parents(fitnesses, population):
    breeding_ratio = 1 / hyperparameters['breeding_rate']
    parent_count = int(len(population) / breeding_ratio)

    fitsum = sum(fitnesses)

    parents = []
    for _ in range(parent_count):
        r = random.uniform(0, fitsum)
        for idx, f in enumerate(fitnesses):
            r -= f
            if r < 0:
                parents.append(population[idx])
                break
    return parents

"""TODO comment
"""
def crossover(couples):
    children = []
    for couple in couples:
        if random.random() < hyperparameters['crossover_rate']:
            x_point = random.randrange(0, len(couple[0]) + 1)
            children.append(couple[0][:x_point] + couple[1][x_point:])
        else:
            children.append(random.choice(couple))
    return children

"""TODO comment
"""
def mutate(children):
    for child in children:
        for feature_idx, feature in enumerate(child):
            for category_idx, _ in enumerate(feature):
                if random.random() < hyperparameters['mutation_rate']:
                    m = random.uniform(-hyperparameters['mutation_range'], hyperparameters['mutation_range'])
                    child[feature_idx][category_idx] += m
    return children

"""TODO comment
"""
def breed(parents):
    pair_count = int(len(parents) / 2)
    couples = list(zip(parents[:pair_count], parents[pair_count:]))

    # if we have an uneven number of parents, the last one is a hermaphrodite
    if len(parents) % 2 != 0:
        couples.append((parents[-1], parents[-1]))

    children = crossover(couples)
    mutate(children)
    return children

"""TODO comment
"""
def poorest_fit_idxs(fitnesses, n):
    idxs = []
    worst_fitnesses = sorted(fitnesses)[:n]
    for i, f in enumerate(fitnesses):
        if f in worst_fitnesses:
            idxs.append(i)
    return idxs

"""TODO comment
"""
def select_survivors(fitnesses, population, children):
    replacement_idxs = poorest_fit_idxs(fitnesses, len(children))
    for i, c in enumerate(children):
        population[replacement_idxs[i]] = c

"""TODO comment
"""
def generation(population, t):
    fitnesses = [t.fitness(chromosome) for chromosome in population]
    parents = select_parents(fitnesses, population)
    children = breed(parents)
    select_survivors(fitnesses, population, children)

if __name__ == '__main__':
    t = Titanic()
    population = t.generate_random_population(hyperparameters['population_size'], hyperparameters['factor_random_min'], hyperparameters['factor_random_max'])
    fitnesses = [t.fitness(chromosome) for chromosome in population]
    print(sum(fitnesses) / len(fitnesses))
    for i in range(hyperparameters['generations']):
        generation(population, t)
        fitnesses = [t.fitness(chromosome) for chromosome in population]
        print(sum(fitnesses) / len(fitnesses))
