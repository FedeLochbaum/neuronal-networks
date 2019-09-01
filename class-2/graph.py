
import copy

start_delimiter_point = 0
end_delimiter_point = 2

# A node is an array of the form 
# [ 
#   [1, 2, 3]
#   [4, 5, 6]
#   [7, 8, 0]
# ]
# and the graph is a dict with { node => { moveSwap => newNode... } }
# moveSwap = { up, down, right, left }

def compute_next_state(node, newX, newY):
  newNode = copy.deepcopy(node)
  x, y = current_target_position(node)
  newNode[x][y] = newNode[newX][newY]
  newNode[newX][newY] = 0
  return newNode

def is_valid_point(point):
  return point >= start_delimiter_point and point <= end_delimiter_point

def current_target_position(node):
  for x in range(len(node)):
    for y in range(len(node[x])):
      if(node[x][y] == 0):
        return x, y
  return None

def is_valid_position(t):
  x, y, d = t
  return is_valid_point(x) and is_valid_point(y)

def possible_movements(node):
  x, y = current_target_position(node)
  next_movements = [(x - 1, y, 'UP'), (x + 1, y, 'DOWN'), (x, y + 1, 'RIGHT'), (x, y - 1, 'LEFT')]
  return list(filter(is_valid_position, next_movements))

class EightProblemGraph:
  def __init__(self):
    self.graph = {}

  def __getitem__(self, node):
    str_node = str(node)
    if str_node not in self.graph:
      self.graph[str_node] = {}
      for newX, newY, direction in possible_movements(node):
        self.graph[str_node].update({ direction: compute_next_state(node, newX, newY) })

    return self.graph[str_node]
