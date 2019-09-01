
start_delimiter_point = 0
end_delimiter_point = 2

def compute_next_state(node, newX, newY):
  newNode = node
  x, y = current_target_position(newNode)
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
  next_movements = [(x + 1, y), 'UP', (x - 1, y, 'DOWN'), (x, y + 1, 'RIGHT'), (x, y - 1, 'LEFT')]
  return list(filter(is_valid_position, next_movements))

class EightProblemGraph:
  def __init__(self):
    self.graph = {}

  def __getattribute__(self, node):
    if node not in self.graph:
      possible_movements = possible_movements(node)
      self.graph[node] = {}
      for newX, newY, direction in possible_movements:
        self.graph[node].update({ direction: compute_next_state(node, newX, newY) })

    return self.graph[node]


# A node is an array of the form 
# [ 
#   [1, 2, 3]
#   [4, 5, 6]
#   [7, 8, 0]
# ]
# and the graph is a dict with { node => { moveSwap => newNode... } }
# moveSwap = { up, down, right, left }

win_node = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 0]
]

# TODO: generate dynamic
initial_node = [
  [4,2,1],
  [8,0,7],
  [6,5,3]
]