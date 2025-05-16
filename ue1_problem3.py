import gurobipy as gp
from gurobipy import GRB

# Problem 3

# not a generic model

comps = ["front", "center", "rear"]
weight_C = [10, 16, 8]
space_C = [6800, 8700, 5300]

cargo = ["C1", "C2", "C3", "C4"]
weight = [18, 15, 23, 12]
volume = [480, 650, 580, 390]
profit = [310, 380, 350, 285]

I = range(len(cargo)) 
J = range(len(comps))

model = gp.Model("LP_model")

x = model.addVars(cargo, comps, vtype=GRB.CONTINUOUS, name="x", lb=0)
y = model.addVars(J, vtype=GRB.CONTINUOUS, name="y", lb=0)

model.setObjective(gp.quicksum(profit[i] * gp.quicksum(x[cargo[i], comps[j]] for j in J) for i in I), GRB.MAXIMIZE)

for i in I:
    model.addConstr(gp.quicksum(x[cargo[i], comps[j]] for j in J) <= weight[i], name="const_resp_weight_{i}")

wp_comps = []
for j in J:
    var = (float)(1 / weight_C[j])
    wp_comps.append(var) 

for j in J:
    model.addConstr(gp.quicksum(x[cargo[i], comps[j]] for i in I) <= weight_C[j], name="const_resp_weightC_{j}")
    model.addConstr(gp.quicksum(volume[i] * x[cargo[i], comps[j]] for i in I) <= space_C[j], name="const_resp_spaceC_{j}")
    model.addConstr(wp_comps[j] * gp.quicksum(x[cargo[i], comps[j]] for i in I) == y[j], name="const_resp_prop_{j}")

model.optimize() # 12151.57895