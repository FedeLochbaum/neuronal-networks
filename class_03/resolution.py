from graph import BlocksWorld
from heuristic import monotonic_abstraction, LOGIC_DESCRIPTION
from a_star import a_star

BLOCKS = ['A', 'B', 'C']

ACTIONS = [
  'pickUp',
  'putDown',
  'stack',
  'unStack'
]

PREDICATES = [
  'on',
  'onTable',
  'clear',
  'holding',
  'empty'
]

def resolve(desc):
  return a_star(BlocksWorld(), desc['initial'], monotonic_abstraction)

print('res: ', resolve(LOGIC_DESCRIPTION))


