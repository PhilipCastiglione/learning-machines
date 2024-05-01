"""TODO comment and properly document
"""
from problems.titanic import Titanic
from algorithms.genetic_algorithm import GeneticAlgorithm

# TODO: get from input, with defaults
hyperparameters = {
    'generations': 200,
    'population_size': 100,
    'breeding_rate': 0.2,
    'crossover_rate': 0.96,
    'mutation_rate': 0.08,
    'mutation_range': 0.1,
}

if __name__ == '__main__':
    # TODO: handle inputs

    t = Titanic()
    g = GeneticAlgorithm(hyperparameters, t)

    while not g.terminate():
        g.next_generation(debug=True)

    g.print_best()
