from graph import BlocksWorld
import a_star

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

LOGIC_DESCRIPTION = {
  'initial': ['onTableA', 'onTableB', 'onTableC', 'empty'],
  'goal': ['onAB', 'onBC', 'empty']
}

# TODO
def monotonic_abstraction(node):
  return 1

def resolve(desc):
  return a_star.a_star(BlocksWorld(), desc['initial'], monotonic_abstraction)
