from graph import EightProblemGraph, current_target_position, compute_next_state, is_valid_position
from functools import reduce
import random
import copy
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
  win_node, path, v = solution
  return simulate(initialNode, path) == win_node

def simulate(initialNode, movements):
  node = copy.deepcopy(initialNode)
  for direction in movements:
    x, y = current_target_position(node)
    newX, newY = next_movement(direction, x, y)
    if(is_valid_position((newX, newY, direction))):
      node = compute_next_state(node, newX, newY)
  return node

def generate_initial_node():
  new_node = copy.deepcopy(win_node)
  possible_movements = ['UP', 'DOWN', 'LEFT', 'RIGHT']
  movements = [random.choice(possible_movements) for i in range(100000)]
  return simulate(new_node, movements)

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
gs_with_h2 = gs.gs(EightProblemGraph(), initial, sum_of_manhattan_distance)
a_star_with_h1 = a_star.a_star(EightProblemGraph(), initial, number_of_wrong_numbers)
a_star_with_h2 = a_star.a_star(EightProblemGraph(), initial, sum_of_manhattan_distance)

print("GS with number_of_wrong_numbers: %s" % (gs_with_h1, ))
if gs_with_h1 != None:
  print('Count of visited nodes: ', gs_with_h1[2])
  print('Checker: ', checker(initial, gs_with_h1))
print('\n')

print("GS with sum_of_manhattan_distance: %s" % (gs_with_h2, ))
if gs_with_h1 != None:
  print('Count of visited nodes: ', gs_with_h2[2])
  print('Checker: ', checker(initial, gs_with_h2))
print('\n')

print("A* with number_of_wrong_numbers: %s" % (a_star_with_h1, ))
if a_star_with_h1 != None:
  print('Count of visited nodes: ', a_star_with_h1[2])
  print('Checker: ', checker(initial, a_star_with_h1))
print('\n')

print("A* with sum_of_manhattan_distance: %s" % (a_star_with_h2, ))
if a_star_with_h2 != None:
  print('Count of visited nodes: ', a_star_with_h2[2])
  print('Checker: ', checker(initial, a_star_with_h2))
print('\n')



