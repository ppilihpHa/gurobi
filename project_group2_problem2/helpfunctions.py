import gurobipy as gp
import pandas as pd
import numpy as np

def preperate_facility_coverage_Matrix(distances, max_distance):
    result = distances.copy()

    N = range(len(distances))

    for i in N:
        for j in N:
            if distances[i][j] <= max_distance:
                result[i][j] = 1
            else:
                result[i][j] = 0
    return result

def getLocations(model, I):
    locations = []
    for i in I:
        locations.append(model.getVarByName(f"x[{i}]").X)
    return locations

def getStations(model, I):
    locations = getLocations(model=model, I=I)
    stations = []
    for index, element in enumerate(locations):
        if element > 0:
            stations.append(index + 1)
    return stations

def getOutput(model, I, distances):
    stations = getStations(model=model, I=I)
    locations = getLocations(model=model, I=I)

    outputDistanceMatrix = pd.DataFrame()
    outputDistanceMatrix.index = stations

    for i,loc in enumerate(locations):
        outputDistanceMatrix[f"District {i + 1}"] = [distances[elem - 1][i] for elem in stations]

    return getOutputMatrix(outputDistanceMatrix, stations, locations)

def getOutputMatrix(outputDistanceMatrix, stations, locations):
    outputMatrix = pd.DataFrame({
        "Covered by" : outputDistanceMatrix.idxmin()
    })
    outputMatrix.index.name = "District"
    outputMatrix.reset_index(inplace=True)
    return outputMatrix

def writeOutput(model, I, distances):
    stations = getStations(model=model,I=I)
    runtime = model.Runtime
    objVal = model.ObjVal

    outputMatrix = getOutput(model=model, I=I, distances=distances)
    summary = pd.DataFrame({
        "information" : ["open stations", "objective Value", "runtime"],
        "value" : [stations, objVal, runtime]
    })

    with pd.ExcelWriter("./project_group2_problem2/output.xlsx", engine="openpyxl") as writer:
        outputMatrix.to_excel(writer, sheet_name="Coverages", index=False)
        summary.to_excel(writer, sheet_name="Summary", index=False)

    return "output.xlsx made"

def genOther(n_district):
    values = np.random.randint(10, 51, size=(n_district, n_district))
    colNames = [f"District {i + 1}" for i in range(n_district)]
    otherDf = pd.DataFrame(values, columns=colNames, index=colNames)
    return otherDf
