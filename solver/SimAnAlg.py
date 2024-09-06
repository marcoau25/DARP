import numpy as np
import random
import matplotlib.pyplot as plt
from solver.cost_computation import cost_function, HopSequences


# Neighbor Generation with two strategies
def enhanced_neighbor_solution(sol):
    new_sol = [v.copy() for v in sol]  # Make a deep copy of the solution
    num_vehicles = len(new_sol)
    
    # Randomly select a type of neighbor generation operation
    operation = random.choice(['swap_between_vehicles', 'reassign_passenger'])

    if operation == 'swap_between_vehicles':
        # Swap passengers between two different vehicles
        v1, v2 = random.sample(range(num_vehicles), 2)
        p1 = [p for p in new_sol[v1] if p != 0]
        p2 = [p for p in new_sol[v2] if p != 0]
        if p1 and p2:
            idx1 = random.randint(0, len(p1) - 1)
            idx2 = random.randint(0, len(p2) - 1)
            new_sol[v1][idx1], new_sol[v2][idx2] = new_sol[v2][idx2], new_sol[v1][idx1]

    elif operation == 'reassign_passenger':
        # Reassign a passenger to another vehicle
        v1, v2 = random.sample(range(num_vehicles), 2)
        p1 = [p for p in new_sol[v1] if p != 0]
        if p1:
            idx1 = random.randint(0, len(p1) - 1)
            # Find first available slot in v2
            for i in range(len(new_sol[v2])):
                if new_sol[v2][i] == 0:
                    new_sol[v2][i] = new_sol[v1][idx1]
                    new_sol[v1][idx1] = 0
                    break
    
    return new_sol

# Adaptive Simulated Annealing with Enhanced Neighboring Function and Cost Tracking
def simulated_annealing_adaptive(starting_sol, G, Vehicles, Requests, RemovedPassengers, initial_temp, final_temp, alpha, iterations):
    current_sol = starting_sol
    current_cost = cost_function(HopSequences(Vehicles, Requests, current_sol, G), RemovedPassengers, G, Requests)
    
    temp = initial_temp
    stagnant_iters = 0  # Track iterations without improvement
    best_sol = current_sol
    best_cost = current_cost
    costs_over_time = []  # List to store the cost at each iteration
    
    while temp > final_temp:
        for i in range(iterations):
            # Generate neighboring solution using enhanced function
            new_sol = enhanced_neighbor_solution(current_sol)
            print(new_sol)
            
            # Calculate cost of new solution
            new_cost = cost_function(HopSequences(Vehicles, Requests, new_sol, G), RemovedPassengers, G, Requests)
            
            delta_cost = new_cost - current_cost
            if delta_cost < 0 or np.exp(-delta_cost / temp) > random.random():
                current_sol = new_sol
                current_cost = new_cost
                stagnant_iters = 0  # Reset stagnant iterations
            else:
                stagnant_iters += 1
            
            # Update best solution if found
            if new_cost < best_cost:
                best_sol = new_sol
                best_cost = new_cost
            
            # Store the cost at this iteration
            costs_over_time.append(current_cost)

        # Adaptive Cooling: If no improvement for 10 iterations, slow down cooling
        if stagnant_iters > 10:
            temp *= 0.99  # Slow cooling down
        else:
            temp *= alpha  # Standard cooling

    return best_sol, best_cost, costs_over_time