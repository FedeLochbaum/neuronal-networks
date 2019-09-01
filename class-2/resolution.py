from graph import EightProblemGraph
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

def manhattan_distance_of(current_value, x, y):
  correct_x, correct_y = position_of_value(current_value)
  # |𝑎−𝑐|+|𝑏−𝑑|
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

# print('graph: ', str(graph.graph))
# print('\n')
# print('graph[initial]: ', str(graph[initial]))
# print('\n')
# print('number_of_wrong_numbers of initial:', number_of_wrong_numbers(initial))
# print('\n')
# print('sum_of_manhattan_distance of initial: ', sum_of_manhattan_distance(initial))
# print('\n')
print("GS with number_of_wrong_numbers: %s" % (gs.gs(EightProblemGraph(), initial, number_of_wrong_numbers),))
print('\n')
# print("GS with sum_of_manhattan_distance: %s" % (gs.gs(EightProblemGraph(), initial, sum_of_manhattan_distance), ))
# print('\n')
