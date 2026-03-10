import pyomo.environ as pyo

a = {
    "kostnad":10,
    "inntekt": 20,
    "co2": 0.45,
    "maling": 10
}

b = {
    "kostnad": 22,
    "inntekt": 28,
    "co2": 0.12,
    "maling": 10
}    

m = pyo.ConcreteModel()





# Beslutningsvariabler
m.a = pyo.Var(domain=pyo.NonNegativeIntegers, initialize=0)
m.b = pyo.Var(domain=pyo.NonNegativeIntegers, initialize=0)

def objective(model):
    netto_a = a["inntekt"] - a["kostnad"]
    netto_b = b["inntekt"] - b["kostnad"]

    return netto_a * model.a + netto_b * model.b

m.obj = pyo.Objective(rule=objective, sense=pyo.maximize)


def total_produksjonskostnad(model):
    return (a["kostnad"] * model.a) + (b["kostnad"] *model.b) <= 10000000

def total_co(model):                                                                       
      return (a["co2"] * model.a) + (b["co2"] * model.b) <= 20000 

def maksimal_maling(model):
    return (a["maling"]/60) * model.a + (b["maling"]/60) * model.b <= 8750

m.total_produksjonskostnad = pyo.Constraint(rule=total_produksjonskostnad)
m.total_co = pyo.Constraint(rule=total_co)
m.maksimal_maling = pyo.Constraint(rule=maksimal_maling)

solver = pyo.SolverFactory("glpk")
result = solver.solve(m, tee=True)


print(f"Status: {result.solver.termination_condition}")
print(f"a: {pyo.value(m.a):.4f}")
print(f"b: {pyo.value(m.b):.4f}")
print(f"Objektiv: {pyo.value(m.obj):.4f}")
