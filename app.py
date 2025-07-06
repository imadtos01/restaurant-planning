import streamlit as st
import pandas as pd
from planning_core import generate_planning

st.set_page_config(page_title="Planning Restaurant", layout="wide")
st.title("📅 Générateur de planning pour restaurant")

# 1️⃣ Charger le fichier de besoins
st.header("1️⃣ Charger le fichier de besoins (Excel)")
uploaded_file = st.file_uploader("Téléverser besoins.xlsx", type=["xlsx"])

if uploaded_file is not None:
    besoins_df = pd.read_excel(uploaded_file, sheet_name=0)
    st.success("✅ Fichier chargé avec succès.")
else:
    st.info("ℹ️ Aucun fichier importé, modèle par défaut utilisé.")
    besoins_df = pd.DataFrame({
        "Heure": [f"{10 + h}:00" for h in range(14)],
        "Lundi": [2]*14,
        "Mardi": [2]*14,
        "Mercredi": [2]*14,
        "Jeudi": [2]*14,
        "Vendredi": [2]*14,
        "Samedi": [3]*14,
        "Dimanche": [3]*14,
    })

# 2️⃣ Modifier les besoins horaires
st.header("2️⃣ Modifier les besoins horaires")
edited_df = st.data_editor(besoins_df, num_rows="dynamic", use_container_width=True)

# 3️⃣ Choix du nombre d'employés
st.header("3️⃣ Nombre d’employés disponibles")
num_workers = st.slider("Sélectionner le nombre d'employés", 1, 20, 6)

# 4️⃣ Bouton pour générer le planning
st.header("4️⃣ Générer le planning")
if st.button("🚀 Lancer la génération"):
    with st.spinner("Optimisation en cours..."):
        # Conversion du dataframe en dictionnaire utilisable
        weekly_chef_need = {}
        for jour in edited_df.columns[1:]:
            weekly_chef_need[jour] = edited_df[jour].tolist()

        output_path = generate_planning(num_workers, weekly_chef_need)

        if output_path:
            st.success("✅ Planning généré avec succès !")
            with open(output_path, "rb") as file:
                st.download_button(
                    label="📥 Télécharger le fichier Excel",
                    data=file,
                    file_name="planning_restaurant.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.error("❌ Échec de l'optimisation. Vérifie les données.")
