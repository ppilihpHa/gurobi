import gurobipy as gp
from gurobipy import GRB

# Model creation

model = gp.Model("LP_model")

# Declaration of Decision Variables

x = model.addVar(vtype=GRB.CONTINUOUS, name="x", lb=0)
y = model.addVar(vtype=GRB.CONTINUOUS, name="y")

# Declaration of Objective Funtion

model.setObjective(2 * x + y, GRB.MAXIMIZE)

# Declaration of Constraints

model.addConstr(2 * x - 5 * y == 0, "Constraint1")
model.addConstr(x + 2 * y >= 9, "Constraint2")
model.addConstr(2 * x + y <= 12, "Constraint3")

# Optimizing

model.optimize()