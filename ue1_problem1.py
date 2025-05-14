import gurobipy as gp
from gurobipy import GRB

# Problem 1

# DV: Amount Product 1 -> x1 | Amount Product 2 -> x2
# c1 -> 10€ | c2 -> 40€
# 3 machines -> ai1, ai2:
    # a11 = 1; a12 = 1; a13 = 3
    # a21 = 5; a22 = 1; a23 = 1
# Capacaty: C1 = 30, C2 = 10, C3 = 24
# maximize income

c1, c2 = 10, 40
a11, a12, a13 = 1, 1, 3
a21 , a22, a23 = 5, 1, 1
C1, C2, C3 = 30, 10, 24

# Model

model = gp.Model("LP_model")

# DV

x1 = model.addVar(vtype=GRB.INTEGER, name="x1", lb=0)
x2 = model.addVar(vtype=GRB.INTEGER, name="x2", lb=0)

# obj. Funciton

model.setObjective(c1 * x1 + c2 * x2, GRB.MAXIMIZE)

# Constraints

model.addConstr(a11 * x1 + a21 * x2 <= C1, "const1")
model.addConstr(a12 * x1 + a22 * x2 <= C2, "const2")
model.addConstr(a13 * x1 + a23 * x2 <= C3, "const3") 

model.optimize() # opt. value = 250
