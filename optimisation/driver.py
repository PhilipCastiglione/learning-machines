"""TODO comment and properly document functions
"""

from problems.dat.titanic import titanic

import random

# from input, with defaults
hyperparameters = {
    'generations': 100,
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

"""Returns a population (list) with randomly initialized chromosomes
"""
def generate_random_population():
    p_size = hyperparameters['population_size']
    return [generate_random_chromosome() for n in range(p_size)]

"""Returns a new random chromosome.
"""
def generate_random_chromosome():
    l = hyperparameters['factor_random_min']
    u = hyperparameters['factor_random_max']
    pclass = [random.uniform(l, u) for i in range(3)]
    sex = [random.uniform(l, u) for i in range(2)]
    age_bucket = [random.uniform(l, u) for i in range(12)]
    siblings_spouses = [random.uniform(l, u) for i in range(9)]
    parents_children = [random.uniform(l, u) for i in range(10)]
    return [pclass, sex, age_bucket, siblings_spouses, parents_children]

"""Calculate and return chromosome fitness.
"""
def fitness(chromosome):
    correct = 0

    for idx, passenger in enumerate(titanic['passengers']):
        # start with the base survival probability then calculate the product
        # with all the chromosome factors
        survival_prob = titanic['average_rate']
        for feature_idx, category_idx in enumerate(passenger):
            survival_prob *= chromosome[feature_idx][category_idx]

        # this is the actual prediction outcome output by the chromosome for
        # this passenger
        survived = 1 if survival_prob > 0.5 else 0

        # if the survival prediction is correct, record it
        if survived == titanic['survival'][idx]:
            correct += 1

    return correct / titanic['n']

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
def generation(population):
    fitnesses = [fitness(chromosome) for chromosome in population]
    parents = select_parents(fitnesses, population)
    children = breed(parents)
    select_survivors(fitnesses, population, children)

if __name__ == '__main__':
    population = generate_random_population()
    fitnesses = [fitness(chromosome) for chromosome in population]
    print(sum(fitnesses) / len(fitnesses))
    for i in range(hyperparameters['generations']):
        generation(population)
        fitnesses = [fitness(chromosome) for chromosome in population]
        print(sum(fitnesses) / len(fitnesses))
