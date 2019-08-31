from collections import deque
import pprint
import dfs
import bfs

def is_goal(t):
  return t == ('', 'CFGW')

initial_node = ('CFGW', '')

# GW => X
# CG => X

LOSE_CASES = ['GW', 'CG']

static_graph = {
  ('CFGW', ''): {
    # 'CF =>': ('GW', 'CF'), X
    'FG =>': ('CW', 'FG'),
    'FW =>': ('CG', 'FW'),
  },
  ('CG', 'FW'): {
    # 'FW <=': ('CFGW', ''), # NO TIENE SENTIDO
    'F <=': ('CFG', 'W'),
  },
  ('CW', 'FG'): {
    'F <=': ('CFW', 'G'),
    # 'FG <=': ('CFGW', ''), # NO TIENE SENTIDO
  },
  ('CFG', 'W'): {
    'FG =>': ('C', 'FGW'),
    'CF =>': ('G', 'CFW'),
  },
  ('CFW', 'G'): {
    'F =>': ('CW', 'FG'),
    'CF =>': ('W', 'CFG'),
    'FW =>': ('C', 'FGW'),
  },
  ('C', 'FGW'): {
    # 'F <=': ('CF', 'GW'), X
    'FG <=': ('CFG', 'W'),
    'FW <=': ('CFW', 'G'),
  },
  ('G', 'CFW'): {
    'F <=': ('FG', 'CW'),
    'CF <=': ('CFG', 'W'),
    'FW <=': ('FGW', 'C')
  },
  ('W', 'CFG'): {
    # 'F <=': ('FW', 'CG'), X
    'CF <=': ('CFW', 'G'),
    'FG <=': ('FGW', 'C'),
  },
  ('FG', 'CW'): {
    'FG =>': ('', 'CFGW'),
    'F =>': ('G', 'CFW')
  },
  ('FGW', 'C'): {
    # 'F =>': ('GW', 'CF'), X
    'FG =>': ('W', 'CFG'),
    'FW =>': ('G', 'CFW')
  }
}

def graph():
  graph = {}
  stack = deque()
  stack.append(('CFGW', ''))
  while(stack):
    left, right = stack.pop()
    if ((left, right) not in graph):
      graph[(left, right)] = {}
    if ('F' in left):
      if 'F =>' not in graph[(left, right)]:
        alone_state = (left.replace('F', ''), ''.join(sorted(right + 'F')))
        stack.append(alone_state)
        graph[(left, right)].update({ 'F =>': alone_state })
      for c in left:
        if c == 'F':
          continue
        else:
          peer = ''.join(sorted('F'+c))
          updated = left.replace('F', '').replace(c, '')
          if updated in LOSE_CASES:
            continue
          newState = updated , ''.join(sorted(right + peer))
          if peer + ' =>' not in graph[(left, right)]:
            graph[(left, right)].update({ peer + ' =>': newState })
            stack.append(newState)
    else:
      if 'F <=' not in graph[(left, right)]:
        alone_state = (''.join(sorted(left + 'F')), right.replace('F', ''))
        stack.append(alone_state)
        graph[(left, right)].update({ 'F <=': alone_state })
      for c in right:
        if c == 'F':
          continue
        else:
          peer = ''.join(sorted('F'+c))
          updated = right.replace('F', '').replace(c, '')
          if updated in LOSE_CASES:
            continue
          newState = ''.join(sorted(left + peer)), updated
          if peer + ' <=' not in graph[(left, right)]:
            graph[(left, right)].update({ peer + ' <=': newState })
            stack.append(newState)
  return graph


print("Initial Graph: %s" % pprint.pprint(static_graph))
print('\n')
print("DFS with static graph: %s" % (dfs.dfs(static_graph, initial_node, is_goal),))
print('\n')
print("BFS with static graph: %s" % (bfs.bfs(static_graph, initial_node, is_goal),))
print('\n')
print("Dynamic Graph: %s" % pprint.pprint(graph()))
print('\n')
print("DFS with dynamic graph: %s" % (dfs.dfs(graph(), initial_node, is_goal),))
print('\n')
print("BFS with dynamic graph: %s" % (bfs.bfs(graph(), initial_node, is_goal),))
