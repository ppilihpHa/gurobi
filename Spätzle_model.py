# Import Gurobilibrary and GRB module
import gurobipy as gp
from gurobipy import GRB

# Create a new model

model = gp.Model("Spaetzle_Pasta")

# Decision variables: x1 (kg of Spaetzle), x2 (kg of Pasta)

x1 = model.addVar(vtype=GRB.CONTINUOUS, name="x1", lb=0) # kg of Spaetzle
x2 = model.addVar(vtype=GRB.CONTINUOUS, name="x2", lb=0) # kg of Pasta

# Objective function: maximize 1.5*x1 + 2*x2

model.setObjective(1.5* x1 + 2* x2, GRB.MAXIMIZE)

# Constraints

model.addConstr(3* x1 + 2* x2 <= 130, "Flour_Capacity") # Capacity of Flour
model.addConstr(x1 + 2* x2 <= 100, "Eggs_Capacity") # Capacity of Eggs
model.addConstr(x1 <= 100, "Spaetzle_Sales_Limit") # Sales limit for Spaetzle
model.addConstr(x2 <= 150, "Pasta_Sales_Limit") # Sales limit for Pasta

# Solve the problem

model.optimize()