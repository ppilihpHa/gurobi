import gurobipy as gp
from gurobipy import GRB

# Problem 2

# not a generic model

# Problem Data

products = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
profits = [8, 7, 5, 2, 2, 10, 10, 10, 10, 6]
time = [5, 2, 4, 3, 3, 3, 3, 3, 5, 3]
material = [21, 49, 22, 28, 31, 41, 43, 36, 31, 37]
demand = [218, 589, 707, 831, 166, 420, 840, 710, 652, 336]
time_C = 200
material_C = 5000
J = list(range(10))
# maximize profit

model = gp.Model("LP_model")

x = model.addVars(J, vtype=GRB.INTEGER, name="x", lb = 0)

model.setObjective(gp.quicksum(profits[i] * x[i] for i in J), GRB.MAXIMIZE)

model.addConstr(gp.quicksum(x[j] * material[j] for j in J) <= material_C, name="mat_Cap")

model.addConstr(gp.quicksum(x[j] * time[j] for j in J) <= time_C, name="time_Cap")

for j in J:
    model.addConstr(x[j] <= demand[j], name=f"demand{j}")

model.optimize() # 700

