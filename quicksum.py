import gurobipy as gp

# math sum in gutobi

I = [1,2,3,4,5,6,7,8,9,10]
val = gp.quicksum(el for el in I)
print(val)
