import random

def nearest_neighbor_tsp(graph):
  """
  Nearest neighbor algorithm for TSP.
  """
  start_node = random.choice(list(graph.nodes()))
  path = [start_node]
  visited = set([start_node])
  while len(visited) < len(graph.nodes()):  # Ensure all nodes are visited
    current_node = path[-1]
    neighbors = [n for n in graph.neighbors(current_node) if n not in visited]
    if not neighbors:  # No unvisited neighbors
      break
    next_node = min(neighbors, key=lambda x: graph[current_node][x]['weight'])
    path.append(next_node)
    visited.add(next_node)
  path.append(start_node)  # Add the starting node to complete the cycle
  return path