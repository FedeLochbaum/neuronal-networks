from collections import deque

def bfs(graph, initialNode, is_goal):
  queue = deque()
  visited = set()
  queue.append((initialNode, []))
  visited.add(initialNode)
  while(queue):
    node, path = queue.popleft()
    if is_goal(node):
      return node, path
    node_edges = graph[node]
    for edge_label, target_node in node_edges.items():
      if target_node not in visited:
        visited.add(target_node)
        queue.append((target_node, path + [edge_label]))
  return None
