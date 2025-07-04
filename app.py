import os
import pandas as pd
from ortools.sat.python import cp_model
from planning_core import generate_planning  # ⬅️ IMPORT DE TES BESOINS

# ───────────────────────── PARAMÈTRES GÉNÉRAUX ────────────────────────────────
DAYS            = 7
HOURS_PER_DAY   = 14
START_HOUR      = 10
num_workers     = 6
max_weekly_hours = 42

weekly_chef_need, besoins_df = generate_planning()  # ⬅️ ON RÉCUPÈRE ICI
day_names = list(weekly_chef_need.keys())

model   = cp_model.CpModel()
idx     = lambda d, h: d * HOURS_PER_DAY + h

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

for w in range(num_workers):
    days_with_break = []
    for d in range(DAYS):
        block_starts = [shifts[w][idx(d, 0)]]
        for h in range(1, HOURS_PER_DAY):
            is_start = model.NewBoolVar(f'start_w{w}_d{d}_h{h}')
            model.AddBoolAnd([shifts[w][idx(d, h)], shifts[w][idx(d, h-1)].Not()]).OnlyEnforceIf(is_start)
            model.AddBoolOr([shifts[w][idx(d, h)].Not(), shifts[w][idx(d, h-1)]]).OnlyEnforceIf(is_start.Not())
            block_starts.append(is_start)
        num_blocks = sum(block_starts)
        model.Add(num_blocks <= 2)
        has_break_today = model.NewBoolVar(f'has_break_w{w}_d{d}')
        model.Add(num_blocks == 2).OnlyEnforceIf(has_break_today)
        model.Add(num_blocks <= 1).OnlyEnforceIf(has_break_today.Not())
        days_with_break.append(has_break_today)
    model.Add(sum(days_with_break) <= 2)

for d in range(DAYS):
    need = weekly_chef_need[day_names[d]]
    for h in range(HOURS_PER_DAY):
        model.Add(sum(shifts[w][idx(d,h)] for w in range(num_workers)) >= need[h])

for w in range(num_workers):
    two_day_blocks = []
    for d in range(DAYS-1):
        b = model.NewBoolVar(f'2off_{w}_{d}')
        model.AddBoolAnd([is_off[w][d], is_off[w][d+1]]).OnlyEnforceIf(b)
        model.AddBoolOr([is_off[w][d].Not(), is_off[w][d+1].Not()]).OnlyEnforceIf(b.Not())
        two_day_blocks.append(b)
    model.Add(sum(two_day_blocks) >= 1)

for w in range(num_workers):
    model.Add(sum(shifts[w]) <= max_weekly_hours)

model.Minimize(sum(shifts[w][h] for w in range(num_workers) for h in range(DAYS * HOURS_PER_DAY)))

solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 20
status = solver.Solve(model)

if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print("❌ Pas de solution.")
    exit()
print("✅ Planning trouvé !")

hour_labels = [f"{(START_HOUR + h) % 24}:00" for h in range(HOURS_PER_DAY)]
summary, planning = [], []

for w in range(num_workers):
    total_hours = working_days = coupures = max_streak = streak = 0
    for d in range(DAYS):
        worked_hours = [h for h in range(HOURS_PER_DAY) if solver.Value(shifts[w][idx(d,h)])]
        if worked_hours:
            working_days += 1
            total_hours += len(worked_hours)
            first, last = worked_hours[0], worked_hours[-1]
            if len(worked_hours) < last - first + 1:
                coupures += 1
        if solver.Value(is_off[w][d]):
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0
        row = {"Employé": f"W{w}", "Jour": day_names[d]}
        row.update({hour_labels[h]: ("✅" if h in worked_hours else "") for h in range(HOURS_PER_DAY)})
        planning.append(row)
    avg = round(total_hours/working_days, 2) if working_days else 0
    summary.append({
        "Employé": f"W{w}",
        "Total heures": total_hours,
        "Jours travaillés": working_days,
        "Heures moy./jour": avg,
        "Nb coupures": coupures,
        "Max jours OFF consécutifs": max_streak
    })

dest = os.path.expanduser("~/Desktop/planning_restaurant.xlsx")
with pd.ExcelWriter(dest) as writer:
    pd.DataFrame(summary).to_excel(writer, sheet_name="Résumé",   index=False)
    pd.DataFrame(planning).to_excel(writer, sheet_name="Planning", index=False)

print(f"📤 Exporté → {dest}")
