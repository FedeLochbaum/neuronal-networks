from a_star import a_star
from graph import ACTIONS, is_valid_op, generateOps
import math

LOGIC_DESCRIPTION = {
  'initial': ['onTableA', 'onTableB', 'onTableC', 'empty', 'clearA', 'clearB', 'clearC'],
  'goal': ['onAB', 'onBC', 'empty']
}

def trivial_heuristic(node):
  if all(goal in node for goal in LOGIC_DESCRIPTION['goal']):
    return 0
  return 1

def monotonic_abstraction(node):
  res = a_star(HeuristicGraph(), node, trivial_heuristic)
  if res == None:
    return math.inf
  return len(res[1])

def operations(node):
  return [ops for action in ACTIONS for ops in list(filter(is_valid_op(node), generateOps(node, action)))]

def compute_next_state(node, operation):
  action, pre, eff_minus, eff_plus = operation
  return list(set(node).union(set(eff_plus)))

class HeuristicGraph:
  def __init__(self):
    self.graph = {}

  def __getitem__(self, node):
    str_node = str(node)
    if str_node not in self.graph:
      self.graph[str_node] = {}
      for op in operations(node):
        self.graph[str_node].update({ op[0]: compute_next_state(node, op) })

    return self.graph[str_node]