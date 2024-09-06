from solver.cost_computation import *
from solver.SimAnAlg import enhanced_neighbor_solution



def tabu_search(Vehicles, Requests, G, initial_solution, RemovedPassengers, tabu_size=5, max_iter=1000):
    # Initial setup
    current_solution = initial_solution
    path_vectors = HopSequences(Vehicles, Requests, current_solution, G)
    current_cost = cost_function(path_vectors, RemovedPassengers=0, graph=G, Requests=Requests)
    best_solution = current_solution
    best_cost = current_cost

    # Tabu list to keep track of recently visited solutions
    tabu_list = []
    
    for iteration in range(max_iter):
        # Generate a neighboring solution
        neighbor_solution = enhanced_neighbor_solution(current_solution)
        neighbor_path_vectors = HopSequences(Vehicles, Requests, neighbor_solution, G)
        neighbor_cost = cost_function(neighbor_path_vectors, RemovedPassengers=0, graph=G, Requests=Requests)

        # Check if the neighbor is the best solution found so far
        if neighbor_cost < best_cost:
            best_solution = neighbor_solution
            best_cost = neighbor_cost

        # Check if the neighbor is better than the current solution or not in the tabu list
        if neighbor_cost < current_cost or (neighbor_solution not in tabu_list):
            current_solution = neighbor_solution
            current_cost = neighbor_cost
            tabu_list.append(current_solution)

        # Maintain the size of the tabu list
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)
    print("TABU LIST:", tabu_list)
    return best_solution, best_cost