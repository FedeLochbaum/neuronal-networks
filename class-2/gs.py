from queue import PriorityQueue

def gs(graph, initialNode, h):
  pqueue = PriorityQueue()
  visited = set()
  pqueue.put(h(initialNode), initialNode, [])
  while not pqueue.empty():
    priority, node, path = pqueue.get_nowait()
    if priority == 0:
      return node, path
    for edge_label, target_node in graph[node].items():
      if target_node not in visited:
        visited.add(target_node)
        pqueue.put((
          h(target_node),
          target_node,
          path + [edge_label]
        ))
  return None
