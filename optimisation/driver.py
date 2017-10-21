"""TODO comment
"""

from problems.dat.titanic import titanic

import random

"""TODO comment
"""
def generate_random_population():
    population_size = 20
    return [generate_random_chromosome() for n in range(population_size)]

"""TODO comment
"""
def generate_random_chromosome():
    l = 0.5
    u = 1.5
    pclass = [random.uniform(l, u) for i in range(3)]
    sex = [random.uniform(l, u) for i in range(2)]
    age_bucket = [random.uniform(l, u) for i in range(12)]
    siblings_spouses = [random.uniform(l, u) for i in range(9)]
    parents_children = [random.uniform(l, u) for i in range(10)]
    return [
        pclass,
        sex,
        age_bucket,
        siblings_spouses,
        parents_children
    ]

"""TODO comment
"""
def fitness(chromosome):
    correct = 0

    for idx, passenger in enumerate(titanic['passengers']):
        # start with the base survival probability then calculate the product
        # with all the chromosome factors
        survival_prob = titanic['average_rate']
        for attr_idx, attr_val in enumerate(passenger):
            survival_prob *= chromosome[attr_idx][attr_val]

        # this is the actual prediction outcome output by the chromosome for
        # this passenger
        survived = 1 if survival_prob > 0.5 else 0

        # if the survival prediction is correct, record it
        if survived == titanic['survival'][idx]:
            correct += 1

    return correct / titanic['n']

if __name__ == '__main__':
    population = generate_random_population()
    for c in population:
        print(fitness(c))
