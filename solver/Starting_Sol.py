import random

#Generation of starting random solution

def GenerateStartingSolution(Requests, Vehicles):
    StartingSolution = [[] for _ in Vehicles]
    
    Vehicles2 = [list(vehicle) for vehicle in Vehicles]
    
    for i in range(len(Requests)):
        
        RandomVehicleIndex = random.randint(0, len(Vehicles)-1)
        
        while Vehicles2[RandomVehicleIndex][1] < 1:
        
            RandomVehicleIndex = random.randint(0, len(Vehicles)-1)
        
        #Assign Request to Vehicle
        
        Vehicles2[RandomVehicleIndex][1] -= 1
        
        StartingSolution[RandomVehicleIndex].append(Requests[i][0])
    
    for i, sublist in enumerate(StartingSolution):
        # i=0
        while len(sublist) < Vehicles[i][1]:
            sublist.append(0)

    return StartingSolution
