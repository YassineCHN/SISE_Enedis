# ============================================================
# 🎨 Style unifié pour l'application GreenTech Solutions
# ============================================================

import streamlit as st

def apply_greentech_style():
    """Applique le style visuel global de l'application (fond, polices, couleurs)."""
    st.markdown(
        """
        <style>
        /* ------------------------------ BASE ------------------------------ */
        html, body, [class*="css"] {
            font-family: "Inter", "Segoe UI", sans-serif;
        }

        .stApp {
            background: #f1f9f4;
            color: #0f4229;
        }

        h1, h2, h3 {
            color: #0f4229;
            font-weight: 800;
        }

        h1 { font-size: 2rem !important; margin-bottom: 0.4em; }
        h2 { font-size: 1.4rem !important; margin-top: 1.2em; }
        h3 { font-size: 1.1rem !important; margin-top: 1em; }

        /* ------------------------------ CARTES ------------------------------ */
        div[data-testid="stVerticalBlock"] > div {
            padding: 0.6rem 1.2rem !important;
        }

        section.main > div {
            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
        }

        /* ------------------------------ TABLES ------------------------------ */
        .dataframe {
            border: 1px solid #d6e8db !important;
            border-radius: 10px !important;
            overflow: hidden;
        }

        .stDataFrame table {
            border-collapse: collapse !important;
        }

        /* ------------------------------ TITRES SIDEBAR ------------------------------ */
        [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: #0f4229 !important;
        }

        /* ------------------------------ BOUTONS ------------------------------ */
        div.stButton > button {
            background: linear-gradient(135deg, #1a7f46, #1b9e55);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1.2rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        div.stButton > button:hover {
            filter: brightness(1.05);
            transform: translateY(-1px);
        }

        /* ------------------------------ EXPANDERS ------------------------------ */
        .streamlit-expanderHeader {
            background: #e6f4ec !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            color: #0f4229 !important;
        }

        /* ------------------------------ SUCCESS / INFO BOXES ------------------------------ */
        .stAlert {
            border-radius: 12px !important;
        }

        /* ------------------------------ FOOTER ------------------------------ */
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )
