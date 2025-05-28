import gurobipy as gp
from gurobipy import GRB

# problem 1 - exc 2

# preprocessing - start

NMats = 3 # N -> # of Materials 
MProducts = 2 # M -> # of Products
N = range(NMats)
M = range(MProducts)

maxMats = [    # (for Product 1, for Product 2) for each Material
    (0.6, 0.6), 
    (0.2, 0.4),
    (0.5, 0.3)
]
minMats = [
    (0.4, 0.5),
    (0.1, 0.1),
    (0.2, 0.2)
]

costMats = [1.0, 1.5, 3.0] # costs for each Material

availableMats = [2_000, 1_000, 500] # available Amounts for each Material

required = [600, 700] # Deman for each Product

price = [10, 8] # selling price for each Product

# preproccesing - end

# gurobi - start

model = gp.Model("LP_model")

# DV: x_ij for Amount of Material i used in Product j
x = model.addVars(NMats, MProducts, vtype=GRB.CONTINUOUS, lb=0, name="x")

# Maximize income -> revenue - costs
model.setObjective(gp.quicksum(price[j] * required[j] for j in M) - gp.quicksum(x[i,j] * costMats[i] for i in N for j in M), GRB.MAXIMIZE)

for j in M:
    model.addConstr((gp.quicksum(x[i,j] for i in N) == required[j]), name=f"satisfy_Demand_{j}") 

for i in N:
    for j in M:
        model.addConstr((x[i,j] <= maxMats[i][j] * required[j]), name=f"respect_max_proportion_{i}")
        model.addConstr((x[i,j] >= minMats[i][j] * required[j]), name=f"respect_min_proportion_{i}")
    model.addConstr(gp.quicksum(x[i,j] for j in M)<= availableMats[i], name=f"respect_availability_{i}")

model.optimize()

# gurobi - end

# postprocessing - start

if model.Status == GRB.OPTIMAL:
    print("Amounts used:")
    for j in M:
        for i in N:
            print(f'{model.getVarByName(f"x[{i},{j}]").X} of material {i} in product {j}')
    print(f"Maximum Income: {model.ObjVal}")
    print(f"Runtime: {model.Runtime}")
else:
    print("No optimal solution found")

# postprocessing - end






