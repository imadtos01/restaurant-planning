import pandas as pd

# Besoins horaires codés en dur
weekly_chef_need = {
    "Monday":    [1, 1, 2, 3, 3, 3, 1, 1, 1, 2, 3, 3, 3, 2],
    "Tuesday":   [1, 1, 2, 3, 3, 3, 1, 1, 1, 2, 3, 3, 3, 2],
    "Wednesday": [1, 1, 2, 3, 4, 4, 1, 1, 1, 2, 3, 4, 4, 2],
    "Thursday":  [1, 1, 2, 3, 4, 4, 1, 1, 1, 2, 3, 4, 4, 2],
    "Friday":    [1, 1, 2, 4, 4, 4, 1, 1, 1, 2, 3, 4, 4, 2],
    "Saturday":  [1, 1, 2, 4, 4, 4, 1, 1, 1, 2, 3, 4, 4, 2],
    "Sunday":    [1, 1, 2, 4, 4, 4, 1, 1, 1, 2, 3, 4, 4, 2],
}

START_HOUR = 10
HOURS_PER_DAY = 14
hour_labels = [f"{(START_HOUR + h) % 24}:00" for h in range(HOURS_PER_DAY)]

besoins_df = pd.DataFrame({
    "Heure": hour_labels,
    "Monday": weekly_chef_need["Monday"],
    "Tuesday": weekly_chef_need["Tuesday"],
    "Wednesday": weekly_chef_need["Wednesday"],
    "Thursday": weekly_chef_need["Thursday"],
    "Friday": weekly_chef_need["Friday"],
    "Saturday": weekly_chef_need["Saturday"],
    "Sunday": weekly_chef_need["Sunday"],
})

def generate_planning():
    return weekly_chef_need, besoins_df
