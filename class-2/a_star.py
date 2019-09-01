from queue import PriorityQueue

# g is the function that receives a node n2 and return the acummulated cost between the initial node n1 and n2
def a_star(graph, initialNode, h, g):
  pqueue = PriorityQueue()
  visited = set()
  pqueue.put((h(initialNode), initialNode, []))
  while not pqueue.empty():
    priority, node, path = pqueue.get_nowait()
    if priority == 0:
      return node, path
    for edge_label, target_node in graph[node].items():
      if str(target_node) not in visited:
        visited.add(str(target_node))
        pqueue.put((
          g(target_node) + h(target_node),
          target_node,
          path + [edge_label]
        ))
  return None
