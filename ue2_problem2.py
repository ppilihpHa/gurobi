import gurobipy as gp
from gurobipy import GRB

# problem 2 - exc 2

# preprocessing - start

crudeOilTypes = ["Crude1", "Crude2", "Crude3"]
n = len(crudeOilTypes)
gasolinTypes = ["Super", "Regular", "Diesel"]
m = len(gasolinTypes)
I = range(n)
J = range(m)

price_Gasoline = [70.0, 60.0, 50.0]
price_Crude = [45.0, 35.0, 25.0]

minOctRating_Gasoline = [10.0, 8.0, 6.0]
maxLeadCont_Gasoline = [0.5, 2.0, 3.5]

octRating_Crude = [12.0, 6.0, 8.0]
leadCont_Crude = [0.5, 2.0, 3.5]

demand_Gasoline = [3000, 2000, 1000]
availability_Crude = [5000, 5000, 5000]
capacity = 14_000

ad_increase = 10

production_cost = 4

# preprocessing - end

# gurobi - start

model = gp.Model("LP_model")

x = model.addVars(I, J, vtype=GRB.CONTINUOUS, lb=0, name="x") # amount crude i used in fuel j
y = model.addVars(J, vtype=GRB.BINARY, name="y") # 0 if fuel j not advertised 1 else
z = model.addVars(J, vtype=GRB.CONTINUOUS, lb=0, name="z") # amount of advertisement for fuel j

model.setObjective(
    (gp.quicksum((demand_Gasoline[j] + (y[j] * z[j] * ad_increase)) * price_Gasoline[j] for j in J)) 
    - 
    (gp.quicksum(x[i,j] * price_Crude[i] for i in I for j in J)), GRB.MAXIMIZE)

model.addConstr(gp.quicksum(x[i, j] for i in I for j in J) <= capacity)

for j in J:
    model.addConstr(gp.quicksum(x[i,j] for i in J) == demand_Gasoline[j] + (y[j] * z[j] * ad_increase), name=f"satisfy_demand_{j}")
    model.addConstr(gp.quicksum(x[i,j] * octRating_Crude[i] for i in I) >= minOctRating_Gasoline[j] * gp.quicksum(x[i, j] for i in I), name="respect_min_oct_{j}") # mean oct >= min oct
    model.addConstr(gp.quicksum(x[i,j] * leadCont_Crude[i] for i in I) <= maxLeadCont_Gasoline[j] * gp.quicksum(x[i,j] for i in I), name="respect_max_lead_{j}") # mean lead <= max lead

for i in I:    
    model.addConstr(gp.quicksum(x[i,j] for j in J) <= availability_Crude[i], name=f"satisfy_availability_{i}")

model.optimize()

# gurobi end

# postprocessing - start

if model.Status == GRB.OPTIMAL:
    print("var values: ")
    for i in I:
        for j in J:
            print(f'amount cruel {i} used in fuel {j}: {model.getVarByName(f"x[{i},{j}]").X}')
    for j in J:
        print(f'amount of advertisemt for fuel {j}: {model.getVarByName(f"z[{j}]").X}')
    print(f"optimal obj. Value: {model.ObjVal}")

# postprocessing - end