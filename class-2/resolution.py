from graph import EightProblemGraph
import random


def generate_initial_node():
  possible_numbers = [i for i in range(9)]
  random.shuffle(possible_numbers)
  return [possible_numbers[0:3], possible_numbers[3:6], possible_numbers[6:9]]

def number_of_wrong_numbers():
  return 2

def sum_of_manhattan_distance():
  return 2




initial = generate_initial_node()
print('random initial state: ', str(initial))
print('\n')

graph = EightProblemGraph()
print('graph: ', str(graph.graph))
print('\n')
print('graph[initial]: ', str(graph[initial]))

