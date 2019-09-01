from graph import EightProblemGraph, current_target_position, compute_next_state
from functools import reduce
import random
import gs
import a_star

######## Win node
win_node = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 0]
]
########

def position_of_value(value):
  for x in range(len(win_node)):
    for y in range(len(win_node[x])):
      if(win_node[x][y] == value):
        return x, y
  return None

def next_movement(direction, x, y):
  result = {
  'UP': lambda x, y: (x - 1, y),
  'DOWN': lambda x, y: (x + 1, y),
  'LEFT': lambda x, y: (x, y - 1),
  'RIGHT': lambda x, y: (x, y + 1),
  }
  return result[direction](x, y)

def checker(initialNode, solution):
  if(solution == None):
    return 'Fail'
  win_node, path = solution
  for direction in path:
    x, y = current_target_position(initialNode)
    newX, newY = next_movement(direction, x, y)
    initialNode = compute_next_state(initialNode, newX, newY)
  return initialNode == win_node

def generate_initial_node():
  possible_numbers = [i for i in range(9)]
  random.shuffle(possible_numbers)
  return [possible_numbers[0:3], possible_numbers[3:6], possible_numbers[6:9]]

def number_of_wrong_numbers(node):
  accum = 0
  for x in range(len(node)):
    for y in range(len(node[x])):
      if(node[x][y] != win_node[x][y]):
        accum+=1
  return accum

# |𝑎−𝑐|+|𝑏−𝑑|
def manhattan_distance_of(current_value, x, y):
  correct_x, correct_y = position_of_value(current_value)
  return abs(x - correct_x) + abs(y - correct_y)
  

def sum_of_manhattan_distance(node):
  accum = 0
  for x in range(len(node)):
    for y in range(len(node[x])):
      accum+= manhattan_distance_of(node[x][y], x, y)
  return accum

initial = generate_initial_node()
print('random initial state: ', str(initial))
print('\n')


gs_with_h1 = gs.gs(EightProblemGraph(), initial, number_of_wrong_numbers)
print("GS with number_of_wrong_numbers: %s" % (gs_with_h1, ))
print('checker: ', checker(initial, gs_with_h1))
print('\n')
# print("GS with sum_of_manhattan_distance: %s" % (gs.gs(EightProblemGraph(), initial, sum_of_manhattan_distance), ))
# print('\n')
