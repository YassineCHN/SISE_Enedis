# scripts/app/utils/data_loader.py
import pandas as pd
import streamlit as st
from pathlib import Path
from app import config

@st.cache_data(show_spinner="Chargement des données...")
def load_data(file_name: str = None, subdir: str = None) -> pd.DataFrame:
    """
    Charge un fichier CSV depuis le dossier data.
    Utilise le cache Streamlit pour plus de performance.
    """
    if file_name is None:
        file_name = config.DEFAULT_DATA_FILE
    if subdir is None:
        subdir = config.DEFAULT_DATA_SUBDIR

    file_path = config.DATA_DIR / subdir / file_name
    if not file_path.exists():
        st.error(f"❌ Fichier introuvable : {file_path}")
        st.stop()

    df = pd.read_csv(file_path)
    return df
