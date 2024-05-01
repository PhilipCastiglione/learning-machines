import csv
import random

"""The titanic dataset contains the details of the passengers who were aboard
the titanic.

This data set used to train models and test their prediction accuracy against
various factors that are correlated against passenger survival.

It's not ideal for genetic algorithms, since difference from 100% accuracy is
better represented by a cost, whereas genetic algorithms can produce fitness
towards an aribitrary unknown limit. However, for a toy problem it doesn't
really matter.
"""
class Titanic:
    """
    Titanic data is imported from a csv file and transformed into the following data
    structure:

    data = {
        'passengers': [
            [
                2,                # travel class 0 - 2
                1,                # sex 0 - 1
                5,                # age bucket 0 - 11 (NB: 0 is unrecorded)
                2,                # siblings/spouses on board 0 - 8
                3                 # parents/children on board 0 - 9
            ], ...
        ],
        'survival: [1, 0, 0 ...], # 1 = survived
        'average_rate': 0.377..,  # the average survival rate of the population
        'n': 1309                 # the size of the population
    }
    """
    def __init__(self):
        self.data = {
            'passengers': [],
            'survival': [],
        }

        self.read_in_data()

    """Transform the contents of the csv file into the data structure."""
    def read_in_data(self):
        with open('./problems/dat/titanic.csv', 'r', encoding='utf-8') as raw_data:
            count = 0
            survivors = 0

            reader = csv.reader(raw_data)
            for row in reader:
                passenger = [int(row[i]) for i in range(0, 5)]
                self.data['passengers'].append(passenger)

                survived = int(row[5])
                self.data['survival'].append(survived)

                count += 1
                survivors += survived

            self.data['average_rate'] = survivors / count
            self.data['n'] = count

    """Returns a new random "solution". A solution is a set of values representing the
    prediction value of the features in the titanic dataset.

    This is a nested data structure matching the passenger data structure, but
    instead of a particular category selection the solution has an array of categories
    with a (multiplicative) value for that category within that factor.

    For example, passenger data includes the travel class of passengers: 1st, 2nd
    or 3rd class.

    The solution contains an array for the travel class feature, say [1.2, 1.0, 0.8].
    This would mean that a passenger in 1st class was 20% more likely to survive,
    whereas a passenger in 3rd class was 20% less likely to survive.

    The range for each feature represents the number of classes relevant to that
    feature. For example while travel class has 3 classes, passenger age has been
    recorded in 12 buckets (one bucket represents unknown age).
    """
    def random_solution(self):
        l_bound = 0.5
        u_bound = 1.5
        pclass = [random.uniform(l_bound, u_bound) for i in range(3)]
        sex = [random.uniform(l_bound, u_bound) for i in range(2)]
        age_bucket = [random.uniform(l_bound, u_bound) for i in range(12)]
        siblings_spouses = [random.uniform(l_bound, u_bound) for i in range(9)]
        parents_children = [random.uniform(l_bound, u_bound) for i in range(10)]
        return [pclass, sex, age_bucket, siblings_spouses, parents_children]

    """Calculate and return solution fitness.

    This is achieved by using the solutions prediction values to estimate each
    passengers survival/death and returning the percentage of correct predctions.
    """
    def fitness(self, solution):
        correct = 0

        for idx, passenger in enumerate(self.data['passengers']):
            # start with the base survival probability then calculate the product
            # with all the solution factors
            survival_prob = self.data['average_rate']
            for feature_idx, category_idx in enumerate(passenger):
                survival_prob *= solution[feature_idx][category_idx]

            # this is the actual prediction outcome output by the solution for
            # this passenger
            survived = 1 if survival_prob > 0.5 else 0

            # if the survival prediction is correct, record it
            if survived == self.data['survival'][idx]:
                correct += 1

        return correct / self.data['n']
