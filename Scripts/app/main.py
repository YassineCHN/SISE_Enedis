# scripts/app/main.py
import sys
from pathlib import Path

# Ajouter le dossier "scripts" au path Python
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
from app.utils.data_loader import load_data

st.set_page_config(page_title="🏠 Tableau de bord Énergie", layout="wide")

st.title("🏠 Tableau de bord énergétique")

# --- Chargement des données ---
df = load_data()

st.subheader("Aperçu des données")
st.dataframe(df.head())

st.success("Application prête ✅")