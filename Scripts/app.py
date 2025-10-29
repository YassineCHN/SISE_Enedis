# app.py - Fichier principal
import streamlit as st
import os
from PIL import Image


# --- Configuration de la page ---
st.set_page_config(
    page_title="Greentech Solutions",
    page_icon="🌱",
    layout="wide"
)

# --- CSS personnalisé : à appliquer le plus tôt possible ---

st.markdown("""
    <style>

    /* 🌿 Fond général - FORCER avec !important */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    .main,
    .block-container {
        background-color: #e9f5ee !important;
    }
    
    /* Forcer le fond pour tous les conteneurs possibles */
    section[data-testid="stAppViewContainer"] > div,
    .element-container {
        background-color: transparent !important;
    }
            
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #e9f5ee !important;
        padding: 10px;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #cce8da !important;
        color: #097536 !important;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s ease-in-out;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #b2dec9 !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #097536 !important;
        color: white !important;
        font-weight: bold;
    }

    /* 🌱 Titre principal */
    .main-title {
        color: #097536 !important;
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.15);
    }

    /* Cartes harmonisées - FORCÉES dès le départ */
    .info-card {
        background-color: #ffffff !important;
        border-radius: 15px !important;
        padding: 25px 30px !important;
        margin: 20px 0 !important;
        box-shadow: 0 4px 10px rgba(9, 117, 54, 0.08) !important;
        border: 1px solid rgba(9, 117, 54, 0.05) !important;
        text-align: left !important;
        color: #094c2e !important;
        transition: all 0.3s ease-in-out !important;
    }
    
    /* FORCER le texte à gauche dans les cartes */
    .info-card h3,
    .info-card p,
    .info-card * {
        text-align: left !important;
    }
    
    /* Effet hover sur les cartes */
    .info-card:hover {
        box-shadow: 0 6px 16px rgba(9, 117, 54, 0.15) !important;
        transform: translateY(-2px) !important;
    }

    /* Si tu utilises des colonnes Streamlit pour les cartes */
    [data-testid="column"] > div {
        background-color: #ffffff !important;
        border-radius: 15px !important;
        padding: 25px 30px !important;
        margin: 20px 0 !important;
        box-shadow: 0 4px 10px rgba(9, 117, 54, 0.08) !important;
        border: 1px solid rgba(9, 117, 54, 0.05) !important;
        transition: all 0.3s ease-in-out !important;
    }
    
    [data-testid="column"] > div:hover {
        box-shadow: 0 6px 16px rgba(9, 117, 54, 0.15) !important;
        transform: translateY(-2px) !important;
    }

    /* Texte global */
    h1, h2, h3, p {
        color: #094c2e !important;
    }

    /* Liens */
    a {
        color: #097536 !important;
        text-decoration: none;
        font-weight: 500;
    }
    a:hover {
        text-decoration: underline;
    }

    /* Masquer la barre latérale */
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="stAppViewContainer"] {
        margin-left: 0 !important;
        padding-left: 0 !important;
    }
    
    /* Forcer le fond sur le header aussi */
    header[data-testid="stHeader"] {
        background-color: #e9f5ee !important;
    }
    
    /* S'assurer que rien ne peut override le fond */
    * {
        scrollbar-color: #097536 #e9f5ee;
    }
        /* Cartes avec gradient subtil */
    .modern-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fdf9 100%) !important;
        border-radius: 20px !important;
        padding: 30px !important;
        margin: 15px 0 !important;
        box-shadow: 0 8px 24px rgba(9, 117, 54, 0.12) !important;
        border: 1px solid rgba(9, 117, 54, 0.08) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-align: left !important;
    }
    
    .modern-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 32px rgba(9, 117, 54, 0.18) !important;
    }
    
    .modern-card h3 {
        color: #097536 !important;
        font-size: 1.4rem !important;
        margin-bottom: 15px !important;
        font-weight: 600 !important;
        text-align: left !important;
    }
    
    .modern-card p, .modern-card ul, .modern-card li {
        color: #2c5f3f !important;
        line-height: 1.7 !important;
        font-size: 1.05rem !important;
        text-align: left !important;
    }
    
    /* Métriques stylées */
    .metric-modern {
        background: linear-gradient(135deg, #ffffff 0%, #eef9f3 100%) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        margin: 10px 0 !important;
        box-shadow: 0 6px 20px rgba(9, 117, 54, 0.1) !important;
        border-left: 4px solid #097536 !important;
        transition: all 0.3s ease !important;
    }
    
    .metric-modern:hover {
        transform: translateX(5px) !important;
        box-shadow: 0 8px 28px rgba(9, 117, 54, 0.15) !important;
    }
    
    .metric-modern h4 {
        color: #097536 !important;
        font-size: 1.15rem !important;
        margin-bottom: 12px !important;
        font-weight: 600 !important;
    }
    
    .metric-value {
        font-size: 1.8rem !important;
        font-weight: bold !important;
        color: #094c2e !important;
        margin: 8px 0 !important;
    }
    
    .metric-detail {
        color: #555 !important;
        font-size: 0.95rem !important;
        margin: 6px 0 !important;
    }
    
    /* Titre avec bordure */
    .section-title {
        color: #097536 !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        margin: 30px 0 20px 0 !important;
        padding-bottom: 10px !important;
        border-bottom: 3px solid #097536 !important;
    }
    
    /* Badges DPE */
    .dpe-badge {
        display: inline-block !important;
        padding: 8px 16px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        margin: 4px !important;
        font-size: 1rem !important;
    }
    
    .dpe-a { background: #007f00 !important; color: white !important; }
    .dpe-b { background: #4CAF50 !important; color: white !important; }
    .dpe-c { background: #CDDC39 !important; color: #333 !important; }
    .dpe-d { background: #FFEB3B !important; color: #333 !important; }
    .dpe-e { background: #FFC107 !important; color: #333 !important; }
    .dpe-f { background: #FF5722 !important; color: white !important; }
    .dpe-g { background: #B71C1C !important; color: white !important; }        
    </style>
""", unsafe_allow_html=True)



# --- Logo principal centré ---
logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo_greentech.png")

if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        st.image(logo, width=300, use_container_width=False)
else:
    st.warning("⚠️ Logo non trouvé. Vérifie qu'il est bien dans le dossier 'assets/logo_greentech.png'.")

# --- Import des modules pour chaque onglet ---
from pages import accueil, statistiques_dpe, simulation, contexte

# --- Création des onglets ---
tab1, tab2, tab3= st.tabs([" Contexte des données", " Statistiques & DPE", " Simulation"])

with tab1:
    contexte.show()
with tab2:
    statistiques_dpe.show()
with tab3:
    simulation.show()
