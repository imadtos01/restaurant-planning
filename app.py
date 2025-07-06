import streamlit as st
import pandas as pd
from planning_core import generate_planning

st.set_page_config(page_title="Planning Restaurant", layout="wide")

st.title("📅 Générateur de planning pour restaurant")

# 📥 Charger les besoins horaires
st.subheader("1️⃣ Charger le fichier de besoins (Excel)")

uploaded_file = st.file_uploader("Téléverser besoins.xlsx", type=["xlsx"])

if uploaded_file:
    besoins_df = pd.read_excel(uploaded_file)
    st.success("✅ Fichier chargé avec succès.")
else:
    besoins_df = pd.read_excel("besoins.xlsx")
    st.info("ℹ️ Aucun fichier importé, modèle par défaut utilisé.")

# 📝 Afficher et modifier les besoins horaires
st.subheader("2️⃣ Modifier les besoins horaires")
editable_df = st.data_editor(besoins_df, use_container_width=True, num_rows="dynamic")

# 📥 Saisie du nombre d'employés
st.subheader("3️⃣ Nombre d’employés disponibles")
num_workers = st.slider("Sélectionner le nombre d'employés", 1, 20, 6)

# 🧠 Générer le planning
st.subheader("4️⃣ Générer le planning")
if st.button("Générer maintenant"):
    # convertir DataFrame en dict
    weekly_chef_need = {
        day: editable_df[day].tolist() for day in editable_df.columns
    }

    output_path = "planning_restaurant.xlsx"
    result = generate_planning(num_workers, weekly_chef_need, output_path)

    if result:
        st.success("✅ Planning généré avec succès !")
        with open(output_path, "rb") as f:
            st.download_button("📥 Télécharger le planning", f, file_name="planning_restaurant.xlsx")
    else:
        st.error("❌ Aucune solution trouvée. Essayez avec des paramètres différents.")
