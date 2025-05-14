import gurobipy as gp
from gurobipy import GRB

# Problem 3

comps = ["front", "center", "rear"]
weight_C = [10, 16, 8]
space_C = [6800, 8700, 5300]

cargo = ["C1", "C2", "C3", "C4"]
weight = [18, 15, 23, 12]
volume = [480, 650, 580, 390]
profit = [310, 380, 350, 285]

J = list(range(4))

model = gp.Model("LP_model")

x = model.addVars(cargo, vtype=GRB.CONTINUOUS, name="cargo", lb=0)

model.setObjective(gp.quicksum(x[j] * profit[j] for j in J), GRB.MAXIMIZE)

