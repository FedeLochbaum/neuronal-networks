
# A node = [PREDICATES]

# An operation has the form = (
#   name: action,
#   pre: [PREDICATES],
#   eff-: [PREDICATES],
#   eff+: [PREDICATES],
# )

# Graph = { node => {
#      operation => node,
#      ...
#   }
# }

BLOCKS = ['A', 'B', 'C']

ACTIONS = [
  'pickUp',
  'putDown',
  'stack',
  'unStack'
]

PREDICATES = [
  #
  # table
  'onTable',
  #
  # block
  'on',
  'clear',
  #
  # hand
  'holding',
  'empty'
]

# action, pre, eff-, eff+

def pickUpOp(block):
  otherBlocks = list(set(BLOCKS) - set(block))
  return ('pickUp' + block, ['empty', 'onTable' + block, 'clear' + block], ['empty', 'onTable' + block, 'on' + block + otherBlocks[0], 'on' + block + otherBlocks[1]], ['holding' + block])

def putDownOp(block):
  return ('putDown' + block, ['holding' + block], ['holding' + block], ['empty', 'onTable' + block, 'clear' + block])

def stackOp(t):
  block1, block2 = t
  return ('stack' + block1 + block2, ['clear' + block2, 'holding' + block1, 'onTable' + block2], ['clear' + block2, 'holding' + block1], ['on' + block1 + block2, 'empty', 'onTable' + block1, 'clear' + block1])

def unStackOp(t):
  block1, block2 = t
  return ('unStack' + block1 + block2, ['on' + block1 + block2, 'onTable' + block1, 'onTable' + block2, 'empty', 'clear' + block1], ['on' + block1 + block2, 'onTable' + block1, 'empty', 'clear' + block1], ['clear' + block2, 'holding' + block1])

op_generator = {
  'pickUp': pickUpOp,
  'putDown': putDownOp,
  'stack': stackOp,
  'unStack': unStackOp,
  }

isBinaryAction = { 'stack': True, 'unStack': True, 'pickUp': False, 'putDown': False }
possibleBinaryCombinations = [('A', 'B'), ('B', 'A'), ('A', 'C'), ('C', 'A'), ('B', 'C'), ('C', 'B')]

is_valid_op = lambda node: lambda op: all(cond in node for cond in op[1])

flatten = lambda l: [item for sublist in l for item in sublist]

def generateByBinaryAction(node, action):
  return list(map(op_generator[action], possibleBinaryCombinations))

def generateByUnaryAction(node, action):
  return list(map(op_generator[action], BLOCKS))

def generateOps(node, action):
  if(isBinaryAction[action]):
    return generateByBinaryAction(node, action)
  return generateByUnaryAction(node, action)

def operations(node):
  return [ops for action in ACTIONS for ops in list(filter(is_valid_op(node), generateOps(node, action)))]

# Si = (Si−1 \ Eff −(oi)) ∪ Eff +(oi).
def compute_next_state(node, operation):
  action, pre, eff_minus, eff_plus = operation
  if is_valid_op(node)(operation):
    return list((set(node) - set(eff_minus)).union(set(eff_plus)))
  return None

class BlocksWorld:
  def __init__(self):
    self.graph = {}

  def __getitem__(self, node):
    str_node = str(node)
    if str_node not in self.graph:
      self.graph[str_node] = {}
      for op in operations(node):
        self.graph[str_node].update({ op[0]: compute_next_state(node, op) })

    return self.graph[str_node]
