# scripts/app/utils/model_utils.py
import joblib
import streamlit as st
from app import config

@st.cache_resource(show_spinner=False)
def load_model(file_name: str = None):
    """
    Charge un modèle sauvegardé (joblib/pickle).
    """
    if file_name is None:
        file_name = config.DEFAULT_MODEL_FILE

    model_path = config.MODEL_DIR / file_name
    if not model_path.exists():
        st.error(f"❌ Modèle introuvable : {model_path}")
        st.stop()

    return joblib.load(model_path)
