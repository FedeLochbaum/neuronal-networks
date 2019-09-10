LOGIC_DESCRIPTION = {
  'initial': ['onTableA', 'onTableB', 'onTableC', 'empty', 'clearA', 'clearB', 'clearC'],
  'goal': ['onAB', 'onBC', 'empty']
}

# TODO
def monotonic_abstraction(node):
  if all(goal in node for goal in LOGIC_DESCRIPTION['goal']):
    return 0
  return 1
