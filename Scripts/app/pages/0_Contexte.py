# ============================================================
# 🌿 PAGE 0 — CONTEXTE (page d’accueil visible dans la sidebar)
# ============================================================
import sys
from pathlib import Path

# ✅ Correction imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # .../Scripts
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from app.utils.ui_style import apply_greentech_style
from app.utils.data_loader import load_data

# --- Configuration Streamlit ---
st.set_page_config(page_title="🏠 Contexte", page_icon="🌱", layout="wide")
apply_greentech_style()

# ============================================================
# 🏠 EN-TÊTE PRINCIPAL
# ============================================================
st.markdown(
    """
    <h1 style='text-align:center; color:#097536; font-weight:800; margin-bottom:0.2em;'>
        🌱 France Énergie – GreenTech Solutions
    </h1>
    <p style='text-align:center; color:#14532d; font-size:1.1rem; margin-top:0;'>
        Vers une meilleure compréhension du Diagnostic de Performance Énergétique
    </p>
    """,
    unsafe_allow_html=True
)

# ============================================================
# 📘 CONTEXTE DU PROJET
# ============================================================
ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
LOGO_FILE = "logo_greentech.png"
DPE_FILE = "dpe.png"

logo_path = ASSETS_DIR / LOGO_FILE
dpe_path = ASSETS_DIR / DPE_FILE

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    else:
        st.warning("🖼️ Logo GreenTech non trouvé dans /Scripts/app/assets")

with col2:
    st.markdown(
        """
        ### Contexte du projet

        **GreenTech Solutions** est une société de services fictive spécialisée dans le développement
        d’applications numériques innovantes pour accompagner la **transition énergétique**.

        🌍 Avec l’accélération du **changement climatique** et la **hausse des prix de l’énergie**, 
        la **sobriété énergétique** devient un enjeu majeur pour les foyers français.  
        C’est pourquoi **Enedis** a sollicité notre équipe pour analyser l’impact du 
        **Diagnostic de Performance Énergétique (DPE)** sur la **consommation électrique des logements**.

        🔹 L’application **France Énergie – GreenTech Solutions** permet :
        - d’**évaluer** la classe DPE d’un logement,  
        - d’**estimer** sa consommation énergétique annuelle,  
        - et de **vérifier** l’éligibilité aux aides **MaPrimeRénov’**.

        <div style='background-color:#f2faf5; padding:12px 16px; border-radius:10px; border:1px solid rgba(9,117,54,0.15); margin-top:12px;'>
        💡 Objectif : rendre la data science accessible pour mieux comprendre et réduire la consommation d’énergie domestique.
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# 🏡 LE DIAGNOSTIC DE PERFORMANCE ÉNERGÉTIQUE (DPE)
# ============================================================
st.markdown("<hr style='margin-top:3rem; margin-bottom:2rem; border:1px solid rgba(9,117,54,0.1);'/>", unsafe_allow_html=True)

st.markdown(
    "<h3 style='color:#065f46; font-weight:800;'>📗 Le Diagnostic de Performance Énergétique (DPE)</h3>",
    unsafe_allow_html=True
)

col_img, col_txt = st.columns([1, 2], gap="large")

with col_img:
    if dpe_path.exists():
        st.image(str(dpe_path), caption="Échelle officielle du DPE", use_container_width=True)
    else:
        st.warning("📉 Image dpe.png non trouvée dans /Scripts/app/assets")

with col_txt:
    html_content = """<div style='background-color:#f4faf5; padding:16px 20px; border-radius:10px; border:1px solid rgba(9,117,54,0.15);'>
<p style='font-size:1.05rem; color:#0f172a;'>
  Le <b>Diagnostic de Performance Énergétique (DPE)</b> permet d’évaluer la performance énergétique d’un logement 
  selon deux critères principaux :
</p>
<ul style='margin-top:0.3em;'>
  <li>🔹 <b>la consommation d’énergie primaire</b> (kWh/m²/an)</li>
  <li>🔹 <b>les émissions de gaz à effet de serre</b> (kg CO₂/m²/an)</li>
</ul>

<p style='margin-top:0.6em;'>
  Il attribue une <b>étiquette énergétique</b> allant de <b>A</b> (logement très performant) à <b>G</b> (logement énergivore).  
  Cet indicateur est désormais <b>opposable</b> : il doit être fourni lors de la <b>vente</b> ou de la <b>location</b> d’un bien immobilier.
</p>

<p style='margin-top:0.6em;'>
  L’objectif de cette application est de permettre à chacun de :
</p>
<ul>
  <li>🌿 <b>comprendre son DPE</b> ;</li>
  <li>⚙️ <b>simuler son évolution</b> selon différents paramètres ;</li>
  <li>💡 <b>mesurer les effets d’une rénovation</b> sur la performance énergétique.</li>
</ul>
</div>"""
    st.markdown(html_content, unsafe_allow_html=True)




# ============================================================
# 📊 APERÇU DES DONNÉES
# ============================================================
st.markdown(
    "<h3 style='color:#065f46; margin-top:2.5rem;'>📊 Aperçu des données</h3>",
    unsafe_allow_html=True
)

try:
    df = load_data()
    st.dataframe(df.head(), use_container_width=True)
    st.caption("Extrait du jeu de données DPE chargé via `data_loader.py`.")
except Exception as e:
    st.error(f"Erreur lors du chargement des données : {e}")
