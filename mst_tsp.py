import networkx as nx

def mst_tsp(graph):
    """
    Minimum Spanning Tree (MST) approach for solving the Traveling Salesman Problem (TSP).
    
    Parameters:
        graph (nx.Graph): Input graph representing the TSP instance.
        
    Returns:
        list: Hamiltonian cycle representing the TSP solution.
    """
    # Step 1: Create a minimum spanning tree
    mst = nx.minimum_spanning_tree(graph)
    first_node = next(iter(graph.nodes())) 
    
    # Step 2: Traverse the minimum spanning tree to generate a tour
    tour = list(nx.dfs_preorder_nodes(mst, first_node))
    
    # Step 3: Convert the tour into a Hamiltonian cycle
    tour.append(tour[0])
    
    return tour