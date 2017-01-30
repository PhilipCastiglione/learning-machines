import nsquare

# TODO: handle args

# TODO: connect the appopriate search algo

# TODO: output to file

# TODO: remove
p1 = [1,2,5,3,4,0,6,7,8]
b1 = nsquare.Board(p1)
print("initial state")
b1.print()
print("goal state")
print(b1.goal_state())
print("possible next states:")
for state in b1.next_states():
    b1.set_state(state)
    b1.print()
    print("---------")

p2 = [6,8,11,0,7,2,15,12,3,10,4,5,9,13,14,1]
b2 = nsquare.Board(p2)
print("initial state")
b2.print()
print("goal state")
print(b2.goal_state())
print("possible next states:")
for state in b2.next_states():
    b2.set_state(state)
    b2.print()
    print("---------")
