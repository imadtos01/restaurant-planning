import pandas as pd
from ortools.sat.python import cp_model
import os

def generate_planning(num_workers, weekly_chef_need, output_path="planning.xlsx"):
    DAYS = 7
    HOURS_PER_DAY = 14
    START_HOUR = 10
    max_weekly_hours = 42

    day_names = list(weekly_chef_need.keys())
    model = cp_model.CpModel()
    idx = lambda d, h: d * HOURS_PER_DAY + h

    shifts = {w: [model.NewBoolVar(f'w{w}_{idx(d,h)}')
                for d in range(DAYS) for h in range(HOURS_PER_DAY)]
            for w in range(num_workers)}

    is_off = {w: [] for w in range(num_workers)}
    for w in range(num_workers):
        for d in range(DAYS):
            off = model.NewBoolVar(f'off_w{w}_d{d}')
            model.Add(sum(shifts[w][idx(d,h)] for h in range(HOURS_PER_DAY)) == 0).OnlyEnforceIf(off)
            model.Add(sum(shifts[w][idx(d,h)] for h in range(HOURS_PER_DAY)) >= 1).OnlyEnforceIf(off.Not())
            is_off[w].append(off)

    # Contrainte de couverture horaire
    for d in range(DAYS):
       need = weekly_chef_need[day_names[d]]


        for h in range(HOURS_PER_DAY):
            model.Add(sum(shifts[w][idx(d,h)] for w in range(num_workers)) >= need[h])

    for w in range(num_workers):
        model.Add(sum(shifts[w]) <= max_weekly_hours)

    model.Minimize(sum(shifts[w][h] for w in range(num_workers) for h in range(DAYS * HOURS_PER_DAY)))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 20
    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None

    hour_labels = [f"{(START_HOUR + h) % 24}:00" for h in range(HOURS_PER_DAY)]
    planning = []

    for w in range(num_workers):
        for d in range(DAYS):
            worked_hours = [h for h in range(HOURS_PER_DAY) if solver.Value(shifts[w][idx(d,h)])]
            row = {"Employé": f"W{w}", "Jour": day_names[d]}
            row.update({hour_labels[h]: ("✅" if h in worked_hours else "") for h in range(HOURS_PER_DAY)})
            planning.append(row)

    df = pd.DataFrame(planning)
    with pd.ExcelWriter(output_path) as writer:
        df.to_excel(writer, index=False, sheet_name="Planning")

    return output_path
