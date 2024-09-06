import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def generate_data(requests_num, vehicle_num):
    Requests = []
    Vehicles = []
    Nodes = []
    
    # Case in which all passengers have different start/stop from the vehicles' origins
    WorstCaseNNodes = requests_num * 2 + vehicle_num 
    
    VehiclePoints = random.sample(range(WorstCaseNNodes), vehicle_num)
    
    Nodes.extend(VehiclePoints)
    
    # Create passengers
    for i in range(requests_num):
        start = random.sample([node for node in range(WorstCaseNNodes) if node not in VehiclePoints and node not in [r[0] for r in Requests]], 1)[0]        
        stop = random.sample([node for node in range(WorstCaseNNodes) if node not in VehiclePoints and node not in [r[1] for r in Requests]], 1)[0]
        PassengersNumber = 1
        penalties = [random.randint(20, 100) for _ in range(4)]
        Requests.append((start, stop, penalties, PassengersNumber))
        Nodes.append(start)
        Nodes.append(stop)
        
    # Create vehicles
    for i in range(vehicle_num):
        origin = VehiclePoints.pop(0)       
        VehicleCapacity = random.randint(2, 12)
        Vehicles.append((origin, VehicleCapacity))
        Nodes.append(origin)
    
    Nodes = list(set(Nodes))
    
    # If total capacity < passengers, drop random requests and count how many passengers are dropped
    TotalCapacity = 0
    RemovedPassengers = 0
    TotalPassengersNumber = 0
    
    for i in range(vehicle_num):
        TotalCapacity += Vehicles[i][1]
        
    for i in range(requests_num):
        TotalPassengersNumber += Requests[i][3]
        
        
    while TotalCapacity < TotalPassengersNumber:
        RemovePassIndex = random.randint(0, len(Requests) - 1)
        RemovedRequest = Requests.pop(RemovePassIndex)
        RemovedPassengers += RemovedRequest[3]
        TotalPassengersNumber -= RemovedPassengers
        
    print(f"Removed {RemovedPassengers} passengers")
        
    return Vehicles, Requests, Nodes, RemovedPassengers
        
    
def createGraphInstance(nodes_list, min_weight_distance, max_weight_distance, min_weight_time, max_weight_time, min_degree):

    # Informative print
    print(f"The current number of nodes is {len(nodes_list)}")

    # Create a graph object
    G = nx.Graph()
    
    # Add starting set: 3 nodes connected by 3 edges
    node1, node2, node3 = random.sample(nodes_list, 3)
    G.add_node(node1)
    G.add_node(node2)
    G.add_node(node3)
    G.add_edge(node1, node2, distance_cost=3, time_cost=12)
    G.add_edge(node1, node3, distance_cost=5, time_cost=20)
    G.add_edge(node2, node3, distance_cost=10, time_cost=30)

    # Add remaining nodes
    for i in range(len(nodes_list)):
        G.add_node(nodes_list[i])
        # Add a number of edges starting from new node equal to min_degree
        for edge in range(min_degree):
            distance_cost = random.randint(min_weight_distance, max_weight_distance)
            time_cost = random.randint(min_weight_time, max_weight_time)
            # Connect the edge to the two previous nodes in the list 
            G.add_edge(nodes_list[i], nodes_list[i - (min_degree - edge)], distance_cost=distance_cost, time_cost=time_cost)

    return G

def visualize_graph(G, vehicles_list, requests_list):
    # Set the figure size
    plt.figure(figsize=(12, 10))

    # Define node positions using spring layout for better visualization
    pos = nx.spring_layout(G)

    # Extract vehicle and request nodes from the lists
    vehicle_nodes = {origin for origin, _ in vehicles_list}
    requests_nodes = {start for start, stop, _, _ in requests_list}
    requests_nodes.update(stop for start, stop, _, _ in requests_list)
    reqs_start = [start for start, _, _, _ in requests_list]

    # Draw nodes for vehicles in one color (e.g., red)
    nx.draw_networkx_nodes(G, pos, nodelist=list(vehicle_nodes), node_size=500, node_color='red', label='Vehicle')

    # Draw nodes for requests in another color (e.g., blue)
    nx.draw_networkx_nodes(G, pos, nodelist=list(requests_nodes), node_size=500, node_color='blue', label='Request')

    # Draw nodes for requests in another color (e.g., blue)
    nx.draw_networkx_nodes(G, pos, nodelist=list(reqs_start), node_size=250, node_color='green', label='Requests Start')

    # Draw edges
    nx.draw_networkx_edges(G, pos, width=2)

    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Draw edge labels with distance and time_cost
    edge_labels = {(u, v): f"{d['distance_cost']}, {d['time_cost']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='green')

    # Show the legend and the graph
    plt.legend()
    plt.title("Graph Visualization with Colored Nodes \n Cost: (Distance, Time)")
    plt.axis('off')
    plt.show()
