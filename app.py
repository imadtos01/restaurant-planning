import streamlit as st
import pandas as pd
from planning_core import generate_planning

# Titre
st.title("📅 Générateur de planning restaurant")

# Étape 1 : Saisir le nombre d’employés
num_workers = st.number_input("Nombre d'employés disponibles", min_value=1, max_value=20, value=6)

# Étape 2 : Modifier les besoins horaires
st.write("### Besoins horaires par jour (nombre minimum d'employés nécessaires chaque heure)")

# Exemple par défaut
default_besoins = {
    "Monday":    [1]*14,
    "Tuesday":   [1]*14,
    "Wednesday": [1]*14,
    "Thursday":  [2]*14,
    "Friday":    [3]*14,
    "Saturday":  [4]*14,
    "Sunday":    [2]*14,
}

# Convertir en DataFrame pour affichage + édition
besoins_df = pd.DataFrame(default_besoins)
besoins_df.index = [f"{10 + i}:00" for i in range(14)]

# Édition interactive
edited_df = st.data_editor(besoins_df, num_rows="fixed")

# Transformer en format dict attendu par generate_planning
weekly_chef_need = {day: edited_df[day].tolist() for day in edited_df.columns}

# Étape 3 : Bouton pour lancer le planning
if st.button("📅 Générer le planning"):
    output_path = "planning_restaurant.xlsx"
    result = generate_planning(num_workers, weekly_chef_need, output_path=output_path)

    if result:
        st.success("✅ Planning généré avec succès !")

        # Télécharger le fichier
        with open(output_path, "rb") as f:
            st.download_button("📥 Télécharger le fichier Excel", f, file_name="planning_restaurant.xlsx")
    else:
        st.error("❌ Aucune solution trouvée. Veuillez ajuster les paramètres.")
