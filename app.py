import streamlit as st
import pandas as pd
import os
from planning_core import generate_planning

st.set_page_config(page_title="Planning Restaurant", layout="wide")
st.title("📅 Générateur de planning pour restaurant")

# 1️⃣ - Upload du fichier Excel
uploaded_file = st.file_uploader("1️⃣ Charger le fichier de besoins (Excel)", type=["xlsx"])
if uploaded_file:
    besoins_df = pd.read_excel(uploaded_file, sheet_name=0, index_col=0)
    st.success("✅ Fichier chargé avec succès.")
else:
    st.info("ℹ️ Aucun fichier importé, modèle par défaut utilisé.")
    besoins_df = pd.read_excel("besoins.xlsx", sheet_name=0, index_col=0)

# 2️⃣ - Modifier les besoins
st.markdown("## 2️⃣ Modifier les besoins horaires")
besoins_df_edit = st.data_editor(besoins_df, use_container_width=True, num_rows="dynamic")

# 3️⃣ - Sélection du nombre d'employés
st.markdown("## 3️⃣ Nombre d’employés disponibles")
num_workers = st.slider("Sélectionner le nombre d'employés", min_value=1, max_value=20, value=6)

# 4️⃣ - Bouton pour générer le planning
if st.button("4️⃣ Générer le planning"):
    weekly_chef_need = {day: list(besoins_df_edit[day].fillna(0).astype(int)) for day in besoins_df_edit.columns}
    output_path = os.path.expanduser("~/planning_restaurant.xlsx")
    result = generate_planning(num_workers, weekly_chef_need, output_path)

    if result:
        st.success("✅ Planning généré avec succès !")
        with open(output_path, "rb") as f:
            st.download_button("📥 Télécharger le planning Excel", f, file_name="planning_restaurant.xlsx")
    else:
        st.error("❌ Une erreur est survenue pendant la génération du planning.")
