from problems.dat.cities import cities

"""Travel is a puzzle where a list of cities in North America must be navigated
in order to find a goal city. The navigation approach presents a problem to be
solved using search algorithms of various strategies.

The distance between cities is provided and a heuristic, straight line distance
is provided to the goal city.

refer: ./cities.py
"""

class Travel:
    """Travel defines the search space, contents and rules for the conceptual
    travel board, and makes itself available through state manipulation for
    search algorithms.
    """

    """Instantiate with an initial state and the board cities."""
    def __init__(self, initial_state):
        self.cities = cities
        self.current_city = initial_state
        # the goal city is fixed as straight line distance data is supplied
        self.goal_city = 'sault ste marie'

    """For debugging."""
    def print(self):
        print("CITIES:")
        print(self.cities)
        print("CURRENTLY IN: {}".format(self.current_city))
        print("GOAL: {}".format(self.goal_city))

    """Returns the current state."""
    def current_state(self):
        return self.current_city

    """Returns the cost of moving from one state to another state. The move
    is assumed to be legal.
    """
    def move_cost(self, state1, state2):
        return self.cities[state1]["neighbours"][state2]

    """Returns the heuristic cost of the current or provided state, determined
    using the straight line distance to the goal city.
    """
    def heuristic_cost(self, state=None):
        # sld => Straight Line Distance
        city = state or self.current_city
        return self.cities[city]["sld"]

    """Returns the legal states available from the current state."""
    def next_states(self):
        return list(self.cities[self.current_city]["neighbours"].keys())

    """Sets the current state."""
    def set_state(self, state):
        self.current_city = state

    """Returns the goal state."""
    def goal_state(self):
        return self.goal_city
