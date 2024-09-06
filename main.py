import numpy as np
import matplotlib.pyplot as plt
from instance_generation.instance_gen import *
from solver.Starting_Sol import *
from solver.cost_computation import cost_function, HopSequences
from solver import SimAnAlg


# Algorithm parameters 
nb_passengers = 15          # Number of passengers  
nb_transfers = 4            # Number of transfers -> consider a capacity from 2 to 12
min_distance = 1            # min distance weight for edges
max_distance = 10			# max distance weight for edges
min_time = 5                # min time weight for edges
max_time = 30               # max time weight for edges
min_degree = 2              # min degree of graph's nodes

# Instance creation
Vehicles, Requests, Nodes, RemovedPassengers = generate_data(nb_passengers, nb_transfers)

G = createGraphInstance(Nodes, min_distance, max_distance, min_time, max_time, min_degree)

StartingSol = GenerateStartingSolution(Requests, Vehicles)

path_vector = HopSequences(Vehicles, Requests, StartingSol, G)


print(cost_function(path_vector, RemovedPassengers, G, Requests))
# visualize_graph(G, Vehicles, Requests)


# Run the SA algorithm

# Parameters
initial_temp = 1000
final_temp = 0.1
alpha = 0.95
iterations = 10

optimized_sol, optimized_cost, costs_over_time = SimAnAlg.simulated_annealing_adaptive(StartingSol, G, Vehicles, Requests, RemovedPassengers, initial_temp, final_temp, alpha, iterations)

print("Optimized Solution:", optimized_sol)
print("Optimized Cost:", optimized_cost)

# Plotting the cost over iterations
plt.plot(costs_over_time)
plt.title("Cost Over Iterations")
plt.xlabel("Iteration")
plt.ylabel("Cost")
plt.show()
