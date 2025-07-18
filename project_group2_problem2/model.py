import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import helpfunctions as hp

model = gp.Model("FacilityLocation")
nOther = int(input("input 0 if you want to solve the case study," \
" input a number > 0 if you want to solve a instance with that number of districts." \
" Walking times then are random between 10 and 50 with the goal of 20 minutes.: "))

# Data-------------------------------------------------------------------------

if nOther == 0:
    data_df = pd.read_excel("./project_group2_problem2/data.xlsx",sheet_name="Distance_Data" ,index_col=0)
else:
    data_df = hp.genOther(nOther).copy()
problem_df = pd.read_excel("./project_group2_problem2/data.xlsx", sheet_name="Problem_Data", index_col=0)

distances = data_df.values 
    # Distance Matrix -> distance from location i to location j
max_distance = problem_df.loc["Max-walking-time", "Value"]
    # Problem specif infomration
coverage = hp.preperate_facility_coverage_Matrix(distances=distances, max_distance=max_distance)
    # -> Matrix | a_ij: 1 if i reachable (max_distance constraint) from j, 0 otherwise

locations = list(data_df.index)
N = len(locations)
I = range(N)
    # -> for iteration

# Decision Variables-----------------------------------------------------------

x = model.addVars(I, vtype=GRB.BINARY, name="x")
    # x = {0,1} | 1, if facility built at location j | 0, else
M = N 
    # Big M -> "large enough artificial variable" | set to maximum number of possibile
    # facilities (facility at every district)

# Modelling--------------------------------------------------------------------

model.setObjective(gp.quicksum(x[j] for j in I), GRB.MINIMIZE)
    # Minimize Number of Facilities -> Optimal number of stations for Mr. Cooper

for i in I:
    model.addConstr(gp.quicksum(x[j] * coverage[i][j] for j in I) >= 1,
                     name=f"every_district_{i}_must_be_covered")
    # >= instead of == for easier solving
    # every district must be reached AND must be reached under max_distance (max_time)

model.optimize()

# postprocessing---------------------------------------------------------------

if model.Status == GRB.OPTIMAL:
    print("\nSee Output.xlsx\nEvaluation:\n")
    print(f"Optimal Number of Stations: {model.ObjVal}")
    print(f"Station in Districts: {hp.getStations(model=model, I=I)}\n")
    print(f"Runtime: {model.Runtime}\n")
    print(hp.writeOutput(model=model, I=I, distances=distances))

# testing

#print(coverage)
