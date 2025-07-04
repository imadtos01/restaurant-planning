import streamlit as st
import pandas as pd
from planning_core import generate_planning

st.set_page_config(page_title="📅 Planning Restaurant", layout="wide")
st.title("📅 Générateur de Planning pour Restaurant")

st.markdown("Modifiez les besoins horaires pour chaque jour, puis cliquez pour générer le planning.")

# Entrée nombre employés
nb_employes = st.number_input("Nombre d'employés disponibles", min_value=1, max_value=20, value=6)
max_heures = st.number_input("Heures max par employé", min_value=10, max_value=60, value=42)

# Tableau des besoins horaires
jours = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
heures = [f"{h}:00" for h in range(10, 24)]
default_data = {jour: [1]*len(heures) for jour in jours}
besoins_df = pd.DataFrame(default_data, index=heures)
edited_df = st.data_editor(besoins_df, use_container_width=True)

# Bouton de génération
if st.button("🚀 Générer le planning"):
    st.info("Calcul en cours...")
    weekly_need = {day: edited_df[day].tolist() for day in jours}

    try:
        generate_planning(
            num_workers=nb_employes,
            weekly_chef_need=weekly_need,
            max_weekly_hours=max_heures,
            output_path="planning.xlsx"
        )
        with open("planning.xlsx", "rb") as f:
            st.download_button("📥 Télécharger le planning Excel", f, file_name="planning.xlsx")
        st.success("✅ Planning généré avec succès !")
    except Exception as e:
        st.error(f"❌ Erreur : {e}")
