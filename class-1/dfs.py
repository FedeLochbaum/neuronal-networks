from collections import deque

def dfs(graph, initialNode, is_goal):
  stack = deque()
  visited = set()
  stack.append((initialNode, []))
  visited.add(initialNode)
  while(stack):
    node, path = stack.pop()
    if is_goal(node):
      return node, path
    node_edges = graph[node]
    for edge_label, target_node in node_edges.items():
      if target_node not in visited:
        visited.add(target_node)
        stack.append((target_node, path + [edge_label]))
  return None
