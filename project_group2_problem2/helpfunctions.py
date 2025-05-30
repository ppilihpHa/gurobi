import gurobipy as gp
import pandas as pd

def preperate_facility_possible_Matrix(distances, max_distance):
    result = distances.copy()

    N = range(len(distances))

    for i in N:
        for j in N:
            if distances[i][j] <= max_distance:
                result[i][j] = 1
#            elif i == j:
#                distances[i][j] = -1
            else:
                result[i][j] = 0
    return result

def getStations(model, J):
    locations = []
    for i in J:
        locations.append(model.getVarByName(f"x[{i}]").X)
    stations = []
    for index, element in enumerate(locations):
        if element > 0:
            stations.append(index + 1)
    return stations

def writeOutput(model, J):
    stations = getStations(model=model,J=J)
    