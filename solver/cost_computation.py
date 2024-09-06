import networkx as nx
import copy


def HopSequences(Vehicles, Requests, Solution, graph):
    # Initialize a list of tuples to store the start and stop points for each vehicle
    path = []
    
    # Create an object for each vehicle where [0] is the list of start and stop points
    Vehicles_obj = [list((list(), list())) for element in Solution]
    
    # Loop through the solution and assign requests to the vehicles
    for i in range(len(Solution)):
        for request in Solution[i]:
            if request != 0:
                # Find the corresponding request from the Requests list
                for node in Requests:
                    if node[0] == request and node not in Vehicles_obj[i]:
                        Vehicles_obj[i][0].append(node[0:2])

    # Create a copy of Vehicles
    Vehicles_copy = Vehicles.copy()
    
    # For each vehicle, compute the path if there are valid requests
    for i in range(len(Vehicles_copy)):
        if len(Vehicles_obj[i][0]) > 0:  # Ensure the vehicle has assigned requests
            path.append(compute_path(Vehicles_obj[i], graph, Vehicles_copy[i]))
        else:
            # Append an empty path or a default value when the vehicle has no requests
            path.append([])  # or path.append([Vehicle_copy[i][0]]) if you want to include the start point

    return path

def compute_path(Vehicle_Requests, graph, Vehicle):
    # If there are no requests for the vehicle, return an empty path
    if len(Vehicle_Requests[0]) == 0:
        return []  # or return [Vehicle[0]] to keep the vehicle's starting point
    
    # Initialize the path and calculate the stops
    path = []
    last_stop = Vehicle_Requests[0][-1][1]
    all_stops = set([stop for start, stop in Vehicle_Requests[0]])
    delivered = list()
    current_node = Vehicle[0]


    # while current_node != last_stop:
    while set(delivered) != all_stops:
        
        path_lenght = []

        for node in Vehicle_Requests[0]:
            
            node = node[0]
            
            #(start, stop)
            
            path_lenght.append(((node,0),nx.dijkstra_path_length(graph, source = current_node, target= node, weight=lambda u, v, d: PathCost(u, v, d))))
            
        for node in Vehicle_Requests[1]:

            #(stop)
            
            path_lenght.append(((node,1), nx.dijkstra_path_length(graph, source = current_node, target= node, weight=lambda u, v, d: PathCost(u, v, d))))
            
        #choose min path

        min_path = min(path_lenght, key=lambda x: x[1])[0]
        path.extend(nx.dijkstra_path(graph, source = current_node, target= min_path[0], weight=lambda u, v, d: PathCost(u, v, d)))
        
        current_node = path[-1]
                
        if min_path[1] == 1:
            path.append(f"Dlvr {min_path[0]}") #delivery
            
            for element in Vehicle_Requests[1]:
                if element == min_path[0]:
                    Vehicle_Requests[1].remove(element)
                    delivered.append(element)

        if min_path[1] == 0:
            path.append(f"Pck {min_path[0]}")   #pickup
            for element in Vehicle_Requests[0]:
                if element[0] == min_path[0]:
                    Vehicle_Requests[0].remove(element)
                    Vehicle_Requests[1].append(element[1])

        
    return path
            
        
def PathCost(u,v,d, w_d = 0.3, w_t = 0.7):
    return w_d * d['distance_cost'] + w_t * d['time_cost']
    
    
def cost_function(path_vectors, RemovedPassengers, graph, Requests, w_d = 0.3, w_t = 0.7, mu1 = 0.1):
    total_cost = 0
        
    for path in path_vectors:
        time = 0
        last_break = 0
        i=0
        while i+1 < len(path):
            current_node = path[i]
            next_node = path[i + 1]
            
            if str(next_node).startswith('Pck'):
                returnValue = process_stop(path[last_break : i+1], 1, time, Requests)
                if returnValue != None:
                    total_cost += returnValue
                    last_break = i+1
                path.remove(path[i+1])
                next_node = path[i]
                current_node = path[i-1]
                
            elif str(next_node).startswith('Dlvr'):
                returnValue = process_stop(path[last_break : i+1], 0, time, Requests)
                if returnValue != None :
                    total_cost += returnValue
                    last_break = i+1
                path.remove(path[i+1])
                next_node = path[i]
                current_node = path[i-1]
            
                # Skip non-integer nodes (pickup/delivery instructions like 'Pck 1', 'Dlvr 1')
            if isinstance(current_node, int) and isinstance(next_node, int):
                # Calculate the cost from current_node to next_node
                edge_data = graph.get_edge_data(current_node, next_node, default=None)
                if edge_data is not None:
                    time += edge_data['time_cost']
                    edge_cost = PathCost(current_node, next_node, edge_data, w_d, w_t)
                    total_cost += edge_cost
                else:
                    #print(f"No edge data between {current_node} and {next_node}.")
                    pass
            else:
                print("RIP")
                
            i=i+1
    
    # Add penalty for removed passengers
    penalty = RemovedPassengers * mu1
    total_cost += penalty
    
    print(f"Total cost: {total_cost}")
    return total_cost
    
    
    
def process_stop(path, flag, time, Requests, early_dlr_pnt = 0.05, late_dlr_pnt = 0.06 , early_pck_pnt = 0.08, late_pck_pnt = 0.09):
        
    if len(path) == 0:
        return None
    
    for element in Requests:
        earliest_dlr = element[2][0]
        latest_dlr = element[2][1]
        earliest_pck = element[2][2]
        latest_pck = element[2][3]
                
        if flag == 1:
            if element[0] == path[-1]:
                
                if earliest_dlr < time < latest_dlr:
                        return 0
                elif time < earliest_dlr:
                    return (earliest_dlr - time) * early_dlr_pnt
                else:
                    return (time - latest_dlr) * late_dlr_pnt
                            
                    
        else:
            if element[1] == path[-1]:
                if earliest_pck < time < latest_pck:
                    return 0
                elif time < earliest_pck:
                    return (earliest_pck - time) * early_pck_pnt
                else:
                    return (time - latest_pck) * late_pck_pnt
    return None
                
    