import csv

"""The titanic dataset contains the details of the passengers who were aboard
the titanic.

This data set used to train models and test their prediction accuracy against
various factors that are correlated against passenger survival.

It's ideal for genetic algorithms, since difference from 100% accuracy is better
represented by a cost, whereas genetic algorithms can produce fitness towards
an aribitrary unknown limit. This isn't really an issue for making toy algos.

The data is imported from a csv file and transformed into the following data
structure:

titanic = {
    'passengers': [
        [
            2,                      # travel class 0 - 2
            1,                      # sex 0 - 1
            5,                      # age bucket 0 - 11 (NB: 0 is unrecorded)
            2,                      # siblings/spouses on board 0 - 8
            3                       # parents/children on board 0 - 9
        ], ...
    ],
    'survival: [1, 0, 1, 1, 0 ...], # 1 = survived
    'average_rate': 0.377..,        # the average survival rate of the population
    'n': 1309                       # the size of the population
}
"""

titanic = {
    'passengers': [],
    'survival': []
}

# transform the contents of the csv file into the data structure
with open('./problems/dat/titanic.csv', 'r', encoding='utf-8') as raw_data:
    count = 0
    survivors = 0

    reader = csv.reader(raw_data)
    for row in reader:
        passenger = [int(row[i]) for i in range(0, 5)]
        titanic['passengers'].append(passenger)

        survived = int(row[5])
        titanic['survival'].append(survived)

        count += 1
        survivors += survived

    titanic['average_rate'] = survivors / count
    titanic['n'] = count
