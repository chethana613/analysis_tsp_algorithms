import matplotlib.pyplot as plt
import networkx as nx
import time
from mst_tsp import mst_tsp
from nearest_neighbor_tsp import nearest_neighbor_tsp
from dataset import parse_dataset

#datasets = ["u724", "pr1002", "pcb1173", "nrw1379", "d2103", "fl3795", "rl5934", "brd14051", "pla33810", "pla85900"]
#optimal_costs = [41910, 259045, 56892, 56638, 80450, 28772, 556045, 469385, 66048945, 142382641]

datasets = ["brd14051"]
optimal_costs = [469385]

cut = 1

def generate_graphs():
    return [[dataset, parse_dataset(dataset)] for dataset in datasets[:cut]]

def tsp(graph, algorithm, results):
    """
    Returns path cost and time taken for the given algorithm.
    """
    start_time = time.time()
    if algorithm == nx.approximation.traveling_salesman.simulated_annealing_tsp:
        path = algorithm(graph, init_cycle="greedy")
    elif algorithm == nx.approximation.traveling_salesman.threshold_accepting_tsp:
        path = algorithm(graph, threshold = 200, max_iterations= 100, init_cycle="greedy")
    else:
        path = algorithm(graph)
    end_time = time.time()
    cost = nx.path_weight(graph, path, weight='weight')
    print(f"{algorithm.__name__:25s} Cost: {cost:5.2f} Time: {end_time - start_time:5.2f}s")
    results[algorithm.__name__] = {"cost": cost, "time": end_time - start_time, "path": path}
    return results

# Step 5: Visualize the solution (optional)
def visualize_solution(G, tour):
    import matplotlib.pyplot as plt
    
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, node_color='lightblue', with_labels=True)
    nx.draw_networkx_edges(G, pos, edgelist=[(tour[i], tour[i+1]) for i in range(len(tour)-1)], edge_color='red')
    nx.draw_networkx_edges(G, pos, edgelist=[(tour[-1], tour[0])], edge_color='red')  # connect last to first
    plt.show()

def plot_cost_vs_iteration(ax, results_list):
    """
    Plots path cost against iteration for each algorithm.
    """
    for algorithm, results in results_list.items():
        costs = [result["cost"] for result in results]
        ax.plot(datasets[:cut], costs, marker='o', label=algorithm)
    ax.plot(datasets[:cut], optimal_costs[:cut], marker='o', label="Optimal")
    
    ax.set_xlabel('Dataset')
    ax.set_ylabel('Cost')
    ax.set_title('Cost vs Dataset')
    ax.grid(True)
    ax.legend()

def plot_time_vs_iteration(ax, results_list):
    """
    Plots time taken against iteration for each algorithm.
    """
    for algorithm, results in results_list.items():
        times = [result["time"] for result in results]
        ax.plot(datasets[:cut], times, marker='o', label=algorithm)
    
    ax.set_xlabel('Dataset')
    ax.set_ylabel('Time (s)')
    ax.set_title('Time taken vs Dataset')
    ax.grid(True)
    ax.legend()
    #ax.set_yscale('log')  # Set y-axis scale to logarithmic

if __name__ == "__main__":
    algorithms = [
        nearest_neighbor_tsp,
        nx.approximation.traveling_salesman.greedy_tsp,
        mst_tsp,
        #nx.approximation.traveling_salesman.christofides,
        nx.approximation.traveling_salesman.simulated_annealing_tsp,
        nx.approximation.traveling_salesman.threshold_accepting_tsp,        
    ]

    results_list = {algorithm.__name__: [] for algorithm in algorithms}
    results = {}

    for i, graph in enumerate(generate_graphs()):
        dataset, G = graph
        print(f"Iteration: {i+1} Dataset: {dataset} Optimal: {optimal_costs[i]}" )

        for algorithm in algorithms:
            results = tsp(G, algorithm, results)
            results_list[algorithm.__name__].append(results[algorithm.__name__])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    plot_cost_vs_iteration(ax1, results_list)
    plot_time_vs_iteration(ax2, results_list)
    
    #plt.tight_layout()
    plt.show()