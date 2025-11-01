import os
import io
import json
import base64
import requests
import streamlit as st
from PIL import Image
from streamlit_lottie import st_lottie

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="DPE • Prédiction étiquette",
    page_icon="✨",
    layout="wide"
)

# -------------------------------
# CSS THEME (Chill / Pro / Night corrigé)
# -------------------------------
def inject_css(mood: str = "Chill"):
    themes = {
        "Chill": {
            "--bg1": "linear-gradient(120deg, #E0EAFC 0%, #CFDEF3 100%)",
            "--glass": "rgba(255,255,255,0.55)",
            "--glass-border": "rgba(255,255,255,0.35)",
            "--text": "#0f172a",
            "--accent": "#5b7fff",
            "--accent-2": "#22c1c3",
            "--btn": "linear-gradient(135deg, #5b7fff, #22c1c3)",
        },
        "Pro": {
            "--bg1": "linear-gradient(120deg, #ECE9E6 0%, #FFFFFF 100%)",
            "--glass": "rgba(255,255,255,0.7)",
            "--glass-border": "rgba(0,0,0,0.06)",
            "--text": "#0b1220",
            "--accent": "#2563eb",
            "--accent-2": "#22c55e",
            "--btn": "linear-gradient(135deg, #2563eb, #22c55e)",
        },
        "Night": {
            "--bg1": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "--glass": "rgba(30,41,59,0.68)",
            "--glass-border": "rgba(255,255,255,0.14)",
            "--text": "#f8fafc",
            "--accent": "#93c5fd",
            "--accent-2": "#6ee7b7",
            "--btn": "linear-gradient(135deg, #60a5fa, #34d399)",
        },
    }
    t = themes.get(mood, themes["Chill"])

    st.markdown(
        f"""
        <style>
        :root {{
            --bg1: {t["--bg1"]};
            --glass: {t["--glass"]};
            --glass-border: {t["--glass-border"]};
            --text: {t["--text"]};
            --accent: {t["--accent"]};
            --accent2: {t["--accent-2"]};
            --btn: {t["--btn"]};
        }}
        body {{ color: var(--text)!important; }}
        .stApp {{
            background: var(--bg1) fixed;
            background-size: 140% 140%;
            animation: moveBg 20s ease infinite;
        }}
        @keyframes moveBg {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        .hero {{
            display: flex;
            gap: 18px;
            align-items: center;
            backdrop-filter: blur(10px);
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: 28px;
            padding: 28px;
            box-shadow: 0 10px 30px rgba(0,0,0,.28);
        }}
        .divider {{
            height: 4px;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--accent), var(--accent2));
            margin: 12px 0;
        }}
        .card {{
            border-radius: 20px;
            padding: 18px;
            background: var(--glass);
            border: 1px solid var(--glass-border);
        }}
        .stNumberInput input, .stTextInput input,
        .stSelectbox div[data-baseweb="select"] {{
            background-color: rgba(255,255,255,0.10)!important;
            color: var(--text)!important;
            border-radius: 12px!important;
            border: 1px solid rgba(255,255,255,0.22)!important;
        }}
        .stNumberInput label, .stSelectbox label, .stTextInput label {{
            color: var(--accent)!important;
            font-weight: 600!important;
        }}
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
            border-bottom: 3px solid var(--accent);
            font-weight: 700;
        }}
        .stButton>button {{
            border: 0;
            color: white !important;
            background: var(--btn);
            border-radius: 14px;
            padding: 0.75rem 1rem;
            font-weight: 700;
            box-shadow: 0 10px 24px rgba(0,0,0,.3);
        }}
        footer {{visibility: hidden;}}
        </style>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------
# LOGO CONFIG
# -------------------------------
from PIL import Image

def load_logo(path_or_url: str):
    try:
        if path_or_url.startswith("http"):
            r = requests.get(path_or_url, timeout=10)
            r.raise_for_status()
            return Image.open(io.BytesIO(r.content))
        return Image.open(path_or_url)
    except Exception:
        return None

def to_base64(img: Image.Image):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

LOGO_SRC = "../assets/logo.png"  # 💡 Mets ton logo ici (ou une URL)
logo_img = load_logo(LOGO_SRC)
logo_b64 = to_base64(logo_img) if logo_img else None

# -------------------------------
# SIDEBAR
# -------------------------------
if logo_img:
    st.sidebar.image(logo_img, caption=None, use_container_width=True)

st.sidebar.header("🎛️ Réglages")
mood = st.sidebar.radio("Thème d’ambiance", ["Chill", "Pro", "Night"], index=0)
inject_css(mood)

default_api_url = os.getenv("API_URL", "http://127.0.0.1:5000/classification")
api_url = st.sidebar.text_input("URL API /classification", value=default_api_url)
use_local = st.sidebar.checkbox("Forcer API locale", value=True)
if use_local:
    api_url = "http://127.0.0.1:5000/classification"

st.sidebar.markdown("---")
st.sidebar.subheader("🎉 Effets")
magic_balloons = st.sidebar.checkbox("Ballons Streamlit", value=True)
use_lottie = st.sidebar.checkbox("Confettis Lottie", value=True)
default_lottie_url = "https://assets9.lottiefiles.com/packages/lf20_qp1q7mct.json"
lottie_url = st.sidebar.text_input("URL Lottie confettis", value=default_lottie_url)
lottie_height = st.sidebar.slider("Hauteur Lottie (px)", 150, 600, 320)
st.sidebar.markdown("---")
show_payload = st.sidebar.checkbox("Voir JSON envoyé", value=False)
show_response = st.sidebar.checkbox("Voir réponse brute", value=False)

# -------------------------------
# LOTTIE LOADER
# -------------------------------
@st.cache_data(show_spinner=False)
def load_lottie_from_url(url: str):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
    except requests.exceptions.RequestException:
        return None
    return None

# -------------------------------
# HERO (AVEC LOGO)
# -------------------------------
if logo_b64:
    st.markdown(
        f"""
        <div class="hero">
            <img src="data:image/png;base64,{logo_b64}" alt="logo"
                 style="width:70px;height:70px;border-radius:14px;box-shadow:0 6px 18px rgba(0,0,0,.25);object-fit:cover;">
            <div>
              <h1 style="margin:0">✨ DPE – Prédiction de l’étiquette</h1>
              <div class="divider"></div>
              <p style="margin-top:6px">
                Estimez la classe énergétique de votre logement à partir de <b>15 variables explicatives</b>.
                Interface relax, effets sympas et résultats instantanés. 😌
              </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="hero">
          <h1 style="margin:0">✨ DPE – Prédiction de l’étiquette</h1>
          <div class="divider"></div>
          <p style="margin-top:6px">
            Estimez la classe énergétique de votre logement à partir de <b>15 variables explicatives</b>.
            Interface relax, effets sympas et résultats instantanés. 😌
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------
# PRESETS D’EXEMPLES
# -------------------------------
presets = {
    "Appartement récent (élec)": dict(
        conso_5_usages_par_m2_ep=240.0, emission_ges_5_usages_par_m2=35.0, conso_5_usages_par_m2_ef=200.0,
        conso_chauffage_ep=7500.0, emission_ges_chauffage=1800.0, cout_chauffage=800.0, besoin_ecs=2300.0,
        surface_habitable_logement=65.0, cout_total_5_usages=1350.0, conso_5_usages_ef_energie_n1=6600.0,
        conso_ecs_ep=1600.0, conso_eclairage_ef=380.0, type_energie_principale_chauffage="Électricité",
        conso_chauffage_ef=5900.0, annee_construction=2015
    ),
    "Maison 1998 (gaz)": dict(
        conso_5_usages_par_m2_ep=280.0, emission_ges_5_usages_par_m2=48.0, conso_5_usages_par_m2_ef=230.0,
        conso_chauffage_ep=8200.0, emission_ges_chauffage=2400.0, cout_chauffage=980.0, besoin_ecs=2700.0,
        surface_habitable_logement=110.0, cout_total_5_usages=1650.0, conso_5_usages_ef_energie_n1=7200.0,
        conso_ecs_ep=1900.0, conso_eclairage_ef=460.0, type_energie_principale_chauffage="Gaz naturel",
        conso_chauffage_ef=6400.0, annee_construction=1998
    ),
    "Studio ancien (fioul)": dict(
        conso_5_usages_par_m2_ep=310.0, emission_ges_5_usages_par_m2=60.0, conso_5_usages_par_m2_ef=260.0,
        conso_chauffage_ep=9000.0, emission_ges_chauffage=3000.0, cout_chauffage=1200.0, besoin_ecs=2800.0,
        surface_habitable_logement=30.0, cout_total_5_usages=1700.0, conso_5_usages_ef_energie_n1=7600.0,
        conso_ecs_ep=2000.0, conso_eclairage_ef=500.0, type_energie_principale_chauffage="Fioul domestique",
        conso_chauffage_ef=6900.0, annee_construction=1972
    ),
}
preset_name = st.selectbox("🧪 Charger un exemple rapide", list(presets.keys()))
preset_vals = presets[preset_name]

# -------------------------------
# TABS
# -------------------------------
tab1, tab2, tab3 = st.tabs(["📝 Saisie", "📊 Résultat", "ℹ️ À propos"])

with tab1:
    st.markdown("#### Remplissez (ou gardez le preset)")

    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            conso_5_usages_par_m2_ep = st.number_input("Conso 5 usages/m² (é. primaire) – kWh/m²",
                0.0, value=preset_vals["conso_5_usages_par_m2_ep"], step=1.0, help="`conso_5_usages_par_m2_ep`")
            emission_ges_5_usages_par_m2 = st.number_input("GES 5 usages/m² – kgCO₂/m²",
                0.0, value=preset_vals["emission_ges_5_usages_par_m2"], step=0.1, help="`emission_ges_5_usages_par_m2`")
            conso_5_usages_par_m2_ef = st.number_input("Conso 5 usages/m² (é. finale) – kWh/m²",
                0.0, value=preset_vals["conso_5_usages_par_m2_ef"], step=1.0, help="`conso_5_usages_par_m2_ef`")
            conso_chauffage_ep = st.number_input("Conso chauffage (é. primaire) – kWh",
                0.0, value=preset_vals["conso_chauffage_ep"], step=10.0, help="`conso_chauffage_ep`")
            emission_ges_chauffage = st.number_input("GES chauffage – kgCO₂",
                0.0, value=preset_vals["emission_ges_chauffage"], step=1.0, help="`emission_ges_chauffage`")

        with col2:
            cout_chauffage = st.number_input("Coût chauffage – €",
                0.0, value=preset_vals["cout_chauffage"], step=1.0, help="`cout_chauffage`")
            besoin_ecs = st.number_input("Besoin ECS – kWh",
                0.0, value=preset_vals["besoin_ecs"], step=10.0, help="`besoin_ecs`")
            surface_habitable_logement = st.number_input("Surface habitable – m²",
                1.0, value=preset_vals["surface_habitable_logement"], step=1.0, help="`surface_habitable_logement`")
            cout_total_5_usages = st.number_input("Coût total 5 usages – €",
                0.0, value=preset_vals["cout_total_5_usages"], step=1.0, help="`cout_total_5_usages`")
            conso_5_usages_ef_energie_n1 = st.number_input("Conso 5 usages (é. finale) – énergie n°1 – kWh",
                0.0, value=preset_vals["conso_5_usages_ef_energie_n1"], step=10.0, help="`conso_5_usages_ef_energie_n1`")

        with col3:
            conso_ecs_ep = st.number_input("Conso ECS (é. primaire) – kWh",
                0.0, value=preset_vals["conso_ecs_ep"], step=10.0, help="`conso_ecs_ep`")
            conso_eclairage_ef = st.number_input("Conso éclairage (é. finale) – kWh",
                0.0, value=preset_vals["conso_eclairage_ef"], step=1.0, help="`conso_eclairage_ef`")
            type_energie_principale_chauffage = st.selectbox(
                "Type d’énergie principale du chauffage",
                [
                    "Électricité", "Gaz naturel", "Charbon", "Bois – Bûches",
                    "Fioul domestique", "Réseau de Chauffage urbain",
                    "Bois – Granulés (pellets) ou briquettes", "Bois – Plaquettes d’industrie",
                    "GPL", "Bois – Plaquettes forestières", "Propane",
                    "Électricité d'origine renouvelable utilisée dans le bâtiment"
                ],
                index=[
                    "Électricité","Gaz naturel","Charbon","Bois – Bûches","Fioul domestique",
                    "Réseau de Chauffage urbain","Bois – Granulés (pellets) ou briquettes",
                    "Bois – Plaquettes d’industrie","GPL","Bois – Plaquettes forestières",
                    "Propane","Électricité d'origine renouvelable utilisée dans le bâtiment"
                ].index(preset_vals["type_energie_principale_chauffage"]),
                help="`type_energie_principale_chauffage`"
            )
            conso_chauffage_ef = st.number_input("Conso chauffage (é. finale) – kWh",
                0.0, value=preset_vals["conso_chauffage_ef"], step=10.0, help="`conso_chauffage_ef`")
            annee_construction = st.number_input("Année de construction",
                1460, 2025, value=int(preset_vals["annee_construction"]), step=1, help="`annee_construction`")

        st.markdown("")
        submit = st.form_submit_button("🔮 Prédire l’étiquette DPE", use_container_width=True)

with tab2:
    ph_res = st.empty()   # placeholder pour le résultat
    ph_fx = st.empty()    # placeholder pour les effets (Lottie)

with tab3:
    st.markdown(
        """
        <div class="card">
            <h3 style="margin-top:0">À propos</h3>
            <p>Cette interface Streamlit interroge une API Flask <code>/classification</code> avec
            15 variables explicatives (consos, GES, coûts, surface, énergie, etc.) et renvoie
            l'étiquette DPE prédite par le modèle scikit-learn.</p>
            <ul>
                <li>🎛️ Trois thèmes d’ambiance : Chill, Pro, Night</li>
                <li>🎈 Ballons & 🎉 Confettis Lottie après une prédiction réussie</li>
                <li>🧪 Presets pour tester en un clic</li>
                <li>🔍 Options pour voir le JSON envoyé et la réponse brute</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------
# PREDICTION CALL
# -------------------------------
if 'last_payload' not in st.session_state:
    st.session_state.last_payload = None

if 'last_pred' not in st.session_state:
    st.session_state.last_pred = None

if submit:
    payload = {
        "conso_5_usages_par_m2_ep": conso_5_usages_par_m2_ep,
        "emission_ges_5_usages_par_m2": emission_ges_5_usages_par_m2,
        "conso_5_usages_par_m2_ef": conso_5_usages_par_m2_ef,
        "conso_chauffage_ep": conso_chauffage_ep,
        "emission_ges_chauffage": emission_ges_chauffage,
        "cout_chauffage": cout_chauffage,
        "besoin_ecs": besoin_ecs,
        "surface_habitable_logement": surface_habitable_logement,
        "cout_total_5_usages": cout_total_5_usages,
        "conso_5_usages_ef_energie_n1": conso_5_usages_ef_energie_n1,
        "conso_ecs_ep": conso_ecs_ep,
        "conso_eclairage_ef": conso_eclairage_ef,
        "type_energie_principale_chauffage": type_energie_principale_chauffage,
        "conso_chauffage_ef": conso_chauffage_ef,
        "annee_construction": int(annee_construction)
    }
    st.session_state.last_payload = payload

    if show_payload:
        with tab2:
            st.markdown("##### 📦 JSON envoyé")
            st.code(json.dumps(payload, ensure_ascii=False, indent=2), language="json")

    with st.spinner("Interrogation de l’API…"):
        try:
            resp = requests.post(api_url, json=payload, timeout=30)

            if show_response:
                with tab2:
                    st.markdown("##### 🧾 Réponse brute")
                    st.text(f"Status: {resp.status_code}")
                    st.text(resp.text)

            if resp.status_code == 200:
                data = resp.json()
                y_pred = data.get("classification")
                st.session_state.last_pred = y_pred

                with tab2:
                    ph_res.success(f"✅ **Étiquette prédite : {y_pred}**")

                # Effets
                if magic_balloons:
                    st.balloons()
                if use_lottie:
                    confetti = load_lottie_from_url(lottie_url)
                    with tab2:
                        if confetti:
                            ph_fx.markdown("")  # reset
                            st_lottie(confetti, height=lottie_height, key="confetti")
                        else:
                            st.info("Impossible de charger l’animation Lottie. Vérifie l’URL.")

            else:
                with tab2:
                    try:
                        err = resp.json()
                    except Exception:
                        err = {"error": resp.text}
                    ph_res.error(f"❌ Erreur {resp.status_code} lors de la prédiction.")
                    st.code(json.dumps(err, ensure_ascii=False, indent=2), language="json")

        except requests.exceptions.RequestException as e:
            with tab2:
                ph_res.error("❌ Impossible de joindre l’API. Vérifie l’URL, le serveur Flask et la connexion.")
                st.exception(e)
