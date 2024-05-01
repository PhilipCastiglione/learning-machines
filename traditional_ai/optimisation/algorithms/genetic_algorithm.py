import random

"""TODO comment and properly document methods
"""

class GeneticAlgorithm:
    """TODO
    """
    def __init__(self, parameters, domain):
        self.breeding_ratio = 1 / parameters['breeding_rate']
        self.crossover_rate = parameters['crossover_rate']
        self.mutation_rate = parameters['mutation_rate']
        self.mutation_range = parameters['mutation_rate']
        self.generations = parameters['generations']
        self.current_generation = 0
        self.population = self.generate_random_population(parameters['population_size'], domain.random_solution)
        self.fitness = domain.fitness
        self.best = None
        self.highest_fitness = 0

    """Print a chromosome to the console."""
    def print_chromosome(self, chromosome):
        for feature in chromosome:
            line = ''
            for category in feature:
                line += "{:.2f} ".format(category)
            print(line)

    """Print the best chromosome within the current population."""
    def print_best(self):
        fitnesses = [self.fitness(chromosome) for chromosome in self.population]
        self.check_new_best(fitnesses)

        print("{:.2f}%".format(self.highest_fitness))
        self.print_chromosome(self.best)

    """Returns a randomly initialized population using the provided chromosome
    generation function.
    """
    def generate_random_population(self, p_size, generate_chromosome):
        return [generate_chromosome() for n in range(p_size)]

    """TODO comment
    NB: We store the best whenever we encounter it because with some parameter
    sets genetic algorithms occasionally spiral backwards into bad outcomes for
    a while lol
    """
    def check_new_best(self, fitnesses):
        highest_current = max(fitnesses)
        if highest_current > self.highest_fitness:
            self.highest_fitness = highest_current
            self.best = self.population[fitnesses.index(highest_current)]

    """TODO comment
    """
    def next_generation(self, debug=False):
        fitnesses = [self.fitness(chromosome) for chromosome in self.population]
        self.check_new_best(fitnesses)
        parents = self.select_parents(fitnesses)
        children = self.breed(parents)
        self.select_survivors(fitnesses, children)
        self.current_generation += 1
        if debug:
            print("{:.2f}%".format(sum(fitnesses) / len(fitnesses)))

    """TODO comment
    """
    def select_parents(self, fitnesses):
        parent_count = int(len(self.population) / self.breeding_ratio)

        fitsum = sum(fitnesses)

        parents = []
        for _ in range(parent_count):
            r = random.uniform(0, fitsum)
            for idx, f in enumerate(fitnesses):
                r -= f
                if r < 0:
                    parents.append(self.population[idx])
                    break
        return parents

    """TODO comment
    """
    def crossover(self, couples):
        children = []
        for couple in couples:
            if random.random() < self.crossover_rate:
                x_point = random.randrange(0, len(couple[0]) + 1)
                children.append(couple[0][:x_point] + couple[1][x_point:])
            else:
                children.append(random.choice(couple))
        return children

    """TODO comment
    """
    def mutate(self, children):
        for child in children:
            for feature_idx, feature in enumerate(child):
                for category_idx, _ in enumerate(feature):
                    if random.random() < self.mutation_rate:
                        m = random.uniform(-self.mutation_range, self.mutation_range)
                        child[feature_idx][category_idx] += m
        return children

    """TODO comment
    """
    def breed(self, parents):
        pair_count = int(len(parents) / 2)
        couples = list(zip(parents[:pair_count], parents[pair_count:]))

        # if we have an uneven number of parents, the last one is a hermaphrodite
        if len(parents) % 2 != 0:
            couples.append((parents[-1], parents[-1]))

        children = self.crossover(couples)
        self.mutate(children)
        return children

    """TODO comment
    """
    def poorest_fit_idxs(self, fitnesses, n):
        idxs = []
        worst_fitnesses = sorted(fitnesses)[:n]
        for i, f in enumerate(fitnesses):
            if f in worst_fitnesses:
                idxs.append(i)
        return idxs

    """TODO comment
    """
    def select_survivors(self, fitnesses, children):
        replacement_idxs = self.poorest_fit_idxs(fitnesses, len(children))
        for i, c in enumerate(children):
            self.population[replacement_idxs[i]] = c

    """TODO comment
    """
    def terminate(self):
        return self.current_generation >= self.generations
