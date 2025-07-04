import streamlit as st
from planning_core import generate_planning

st.set_page_config(page_title="Planning Restaurant", layout="wide")

st.title("📅 Générateur de planning pour restaurant")

# Appel de ta fonction dans planning_core
weekly_chef_need, besoins_df = generate_planning()

st.header("📊 Besoins horaires hebdomadaires des chefs")
st.dataframe(besoins_df.style.highlight_max(axis=0), use_container_width=True)

st.markdown("---")
st.info(
    """
    Cette application affiche le besoin en chefs par jour et par créneau horaire.
    Les besoins sont codés en dur dans le module `planning_core.py`.
    """
)
