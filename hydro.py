import csv
import pyomo.environ as pyo
import math

# ===== Les data =====

def read_csv(filename):
    with open(filename) as f:
        reader = csv.DictReader(f)
        return {int(row[reader.fieldnames[0]]): {k: float(v) for k, v in row.items() if k != reader.fieldnames[0]}
                for row in reader}

materials = read_csv("materials.csv")
orders = read_csv("orders.csv")

FURNACE_CAPACITY = 25  # tonn
ELEMENTS = ["Si", "Fe", "Mg"]
M = list(materials.keys())
O = list(orders.keys())


# ===== DEL 1: Produksjonsplan for 1 charge (Ordre 1) =====

print("=" * 60)
print("DEL 1 — Produksjonsplan for 1 charge (Ordre 1)")
print("=" * 60)

order_id = 1
order = orders[order_id]
charge_size = min(order["weight"], FURNACE_CAPACITY)

m1 = pyo.ConcreteModel()
m1.M = pyo.Set(initialize=M)
m1.x = pyo.Var(m1.M, domain=pyo.NonNegativeReals, initialize=0)

m1.obj = pyo.Objective(
    expr=sum(materials[i]["value"] * m1.x[i] for i in M),
    sense=pyo.minimize
)

m1.weight = pyo.Constraint(
    expr=sum(m1.x[i] for i in M) == charge_size
)

m1.stock_c = pyo.ConstraintList()
for i in M:
    m1.stock_c.add(m1.x[i] <= materials[i]["stock"])

m1.chem = pyo.ConstraintList()
for elem in ELEMENTS:
    content = sum(materials[i][f"{elem}_perc"] / 100 * m1.x[i] for i in M)
    m1.chem.add(content >= order[f"{elem}_min"] / 100 * charge_size)
    m1.chem.add(content <= order[f"{elem}_max"] / 100 * charge_size)

solver = pyo.SolverFactory("glpk")
r1 = solver.solve(m1)

print(f"Status: {r1.solver.termination_condition}")
print(f"Charge størrelse: {charge_size} tonn\n")
print(f"{'Material':>10} | {'Mengde (tonn)':>14} | {'Kostnad (kr)':>12}")
print("-" * 43)
for i in M:
    v = pyo.value(m1.x[i])
    if v and v > 0.001:
        print(f"{i:>10} | {v:>14.4f} | {materials[i]['value'] * v:>12.2f}")
print(f"\nTotal kostnad: {pyo.value(m1.obj):.2f} kr")

print("\nKjemisk sammensetning:")
for elem in ELEMENTS:
    pct = sum(materials[i][f"{elem}_perc"] / 100 * pyo.value(m1.x[i]) for i in M) / charge_size * 100
    lo, hi = order[f"{elem}_min"], order[f"{elem}_max"]
    print(f"  {elem}: {pct:.3f}%  (krav: {lo}% – {hi}%)")


# ===== DEL 2: Produksjonsplaner for alle ordre =====

print("\n" + "=" * 60)
print("DEL 2 — Produksjonsplaner for alle ordre (delt lager)")
print("=" * 60)

m2 = pyo.ConcreteModel()
m2.O = pyo.Set(initialize=O)
m2.M = pyo.Set(initialize=M)
m2.x = pyo.Var(m2.O, m2.M, domain=pyo.NonNegativeReals, initialize=0)

m2.obj = pyo.Objective(
    expr=sum(materials[i]["value"] * m2.x[o, i] for o in O for i in M),
    sense=pyo.minimize
)

m2.weight = pyo.ConstraintList()
for o in O:
    m2.weight.add(sum(m2.x[o, i] for i in M) == orders[o]["weight"])

m2.stock_c = pyo.ConstraintList()
for i in M:
    m2.stock_c.add(sum(m2.x[o, i] for o in O) <= materials[i]["stock"])

m2.chem = pyo.ConstraintList()
for o in O:
    w = orders[o]["weight"]
    for elem in ELEMENTS:
        content = sum(materials[i][f"{elem}_perc"] / 100 * m2.x[o, i] for i in M)
        m2.chem.add(content >= orders[o][f"{elem}_min"] / 100 * w)
        m2.chem.add(content <= orders[o][f"{elem}_max"] / 100 * w)

r2 = solver.solve(m2)

print(f"\nStatus: {r2.solver.termination_condition}")
print(f"Total kostnad alle ordre: {pyo.value(m2.obj):.2f} kr")

for o in O:
    w = orders[o]["weight"]
    n_charges = math.ceil(w / FURNACE_CAPACITY)
    print(f"\n--- Ordre {o} ({w} tonn → {n_charges} charge{'r' if n_charges > 1 else ''} à {w/n_charges:.1f} tonn) ---")
    print(f"  {'Material':>10} | {'Totalt (tonn)':>13} | {'Per charge (tonn)':>17}")
    print("  " + "-" * 47)
    for i in M:
        v = pyo.value(m2.x[o, i])
        if v and v > 0.001:
            print(f"  {i:>10} | {v:>13.4f} | {v / n_charges:>17.4f}")
    print(f"  Kjemisk sammensetning:")
    for elem in ELEMENTS:
        pct = sum(materials[i][f"{elem}_perc"] / 100 * pyo.value(m2.x[o, i]) for i in M) / w * 100
        lo, hi = orders[o][f"{elem}_min"], orders[o][f"{elem}_max"]
        print(f"    {elem}: {pct:.3f}%  (krav: {lo}% – {hi}%)")
