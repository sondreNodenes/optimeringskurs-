import pyomo.environ as pyo

kontorer = {
    "Lahore":       {"x": 31.30, "y": 74.18, "cost": 0.3},
    "Islamabad":    {"x": 33.70, "y": 73.05, "cost": 0.2},
    "Muzaffarabad": {"x": 34.31, "y": 73.57, "cost": 10.0},
    "Peshawar":     {"x": 33.96, "y": 71.49, "cost": 0.8},
}

m = pyo.ConcreteModel()

# Beslutningsvariabler
m.x = pyo.Var(domain=pyo.Reals, initialize=0.0)
m.y = pyo.Var(domain=pyo.Reals, initialize=0.0)

# Objektivfunksjon
def objective(model):
    return sum(
        kontorer[k]["cost"] * pyo.sqrt(
            (model.x - kontorer[k]["x"])**2 +
            (model.y - kontorer[k]["y"])**2
        )
        for k in kontorer
    )

m.obj = pyo.Objective(rule=objective, sense=pyo.minimize)

# Constraints
def west_constraint_rule(model):
    return 1.17 * model.x + 0.27 * model.y <= 94.53

m.west_constraint = pyo.Constraint(rule=west_constraint_rule)

# Solve
solver = pyo.SolverFactory("ipopt")
result = solver.solve(m, tee=True)

# Results
print("\nStatus:", result.solver.status)
print("Termination condition:", result.solver.termination_condition)

print(f"\nOptimal lokasjon:")
print(f"x (nord): {pyo.value(m.x):.4f}")
print(f"y (øst):  {pyo.value(m.y):.4f}")

print(f"\nMinimum kostnad: {pyo.value(m.obj):.6f}")

print("\nAvstander og kostnadsbidrag:")
for k in kontorer:
    dist = ((pyo.value(m.x) - kontorer[k]["x"])**2 + (pyo.value(m.y) - kontorer[k]["y"])**2)**0.5
    bidrag = kontorer[k]["cost"] * dist
    print(f"{k:12s} | avstand = {dist:.4f} | kostnadsbidrag = {bidrag:.4f}")