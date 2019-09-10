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
  'initial': ['onTableA', 'onTableB', 'onTableC', 'empty', 'clearA', 'clearB', 'clearC'],
  'goal': ['onAB', 'onBC', 'empty']
}

# TODO
def monotonic_abstraction(node):
  if all(goal in node for goal in LOGIC_DESCRIPTION['goal']):
    return 0
  return 1

def resolve(desc):
  return a_star.a_star(BlocksWorld(), desc['initial'], monotonic_abstraction)


g = BlocksWorld()

print('res: ', a_star.a_star(g, LOGIC_DESCRIPTION['initial'], monotonic_abstraction))

print('\n')

# print('graph: ', str(g.graph.keys()))

