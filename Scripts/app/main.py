# ============================================================
# 🏠 Point d'entrée – France Énergie / GreenTech Solutions
# ============================================================
import sys
from pathlib import Path

# ✅ 1) Rendre importable le package "app" depuis toutes les pages
PROJECT_ROOT = Path(__file__).resolve().parents[1]   # .../Scripts
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
st.set_page_config(page_title="France Énergie – GreenTech Solutions", page_icon="🌿", layout="wide")

from app.utils.ui_style import apply_greentech_style
apply_greentech_style()

# Message d’accueil simple (cette page ne figure plus dans la sidebar
# si tu utilises les pages numérotées dans /pages/, comme 0_Contexte.py)
st.markdown("""
<div style='text-align:center; padding:64px 0;'>
  <h1 style='color:#097536; font-weight:800;'>🌿 France Énergie – GreenTech Solutions</h1>
  <p style='font-size:1.1rem; color:#14532d; margin-top:.5rem;'>Utilisez le menu à gauche pour naviguer.</p>
  <ul style='list-style:none; padding:0; font-size:1.05rem; line-height:1.8;'>
    <li>🏠 <b>Contexte</b> — Présentation</li>
    <li>🔍 <b>Exploration</b> — Données et filtres</li>
    <li>📊 <b>Analyse</b> — Visualisations</li>
    <li>🗺️ <b>Cartographie</b></li>
    <li>⚡ <b>Prédiction</b></li>
    <li>👥 <b>Profils</b></li>
  </ul>
</div>
""", unsafe_allow_html=True)
