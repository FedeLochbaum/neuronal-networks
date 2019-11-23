from queue import PriorityQueue

def a_star(graph, initialNode, h):
  pqueue = PriorityQueue()
  visited = set()
  pqueue.put((h(initialNode), initialNode, []))
  while not pqueue.empty():
    priority, node, path = pqueue.get_nowait()
    if h(node) == 0:
      return node, path, len(visited)
    for edge_label, target_node in graph[node].items():
      if str(target_node) not in visited:
        visited.add(str(target_node))
        pqueue.put((
          priority + h(target_node),
          target_node,
          path + [edge_label]
        ))
  return None
