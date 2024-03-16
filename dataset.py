import networkx as nx
import numpy as np

def parse_tsplib(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    coordinates = {}
    reading_coordinates = False

    
    for line in lines:
        line = line.strip()  # Remove leading and trailing whitespaces, including '\n'
        if line.startswith('NODE_COORD_SECTION'):
            reading_coordinates = True
            continue
        if line.startswith('EOF'):
            break
        if (reading_coordinates):
            parts = line.split()
            if len(parts) == 3:
                node_id = int(parts[0])
                x_coord = float(parts[1])
                y_coord = float(parts[2])
                coordinates[node_id] = (x_coord, y_coord)

    return coordinates

def create_graph(coordinates):
    G = nx.Graph()
    for node, coord in coordinates.items():
        G.add_node(node, pos=coord)

    # Convert coordinates dictionary to array
    coords_array = np.array(list(coordinates.values()))

    # Compute pairwise distances using NumPy broadcasting
    x_diff = coords_array[:, 0][:, np.newaxis] - coords_array[:, 0]
    y_diff = coords_array[:, 1][:, np.newaxis] - coords_array[:, 1]
    distances = np.sqrt(x_diff**2 + y_diff**2)

    # Add edges to the graph
    num_nodes = len(coordinates)
    for u in range(num_nodes):
        for v in range(u + 1, num_nodes):  # Ensure we calculate each edge only once
            distance = distances[u, v]
            G.add_edge(u+1, v+1, weight=distance)
        print(u)

    return G

def parse_dataset(filename):
    coordinates = parse_tsplib("datasets/" + filename + ".tsp")
    return create_graph(coordinates)
