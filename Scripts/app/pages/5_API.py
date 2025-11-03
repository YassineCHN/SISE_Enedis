# ============================================================
# 🔌 PAGE 5 — API
# Documentation et interface de test pour l'API SISE_Enedis
# ============================================================
from app.utils.ui_style import apply_greentech_style
import streamlit as st
import requests
import pandas as pd
import json
import time

st.set_page_config(page_title="API SISE_Enedis", page_icon="🔌", layout="wide")
apply_greentech_style()

# ---------- Small CSS ----------
st.markdown("""
<style>
.badge{display:inline-block;padding:2px 8px;border-radius:12px;font-size:0.8rem;font-weight:700}
.badge-get{background:#E6F4EA;color:#137333;border:1px solid #B7E1CD}
.badge-post{background:#E8F0FE;color:#174EA6;border:1px solid #C6DAFC}
.badge-url{background:#FFF7E6;color:#8D5A00;border:1px solid #FFE0B2}
.small{font-size:.9rem}
hr{border:none;border-top:1px solid #eee;margin:16px 0}
</style>
""", unsafe_allow_html=True)

st.title("🔌 API — Documentation & Outil de Requête (SISE_Enedis)")
st.markdown("Cette page permet d’explorer et de tester les endpoints de l’API locale utilisée par les modèles de prédiction.")

# ---------- Base URL ----------
st.subheader("URL de base")
colA, colB = st.columns([2, 1])
with colA:
    api_url = st.text_input(
        "Base URL de l'API",
        value="http://127.0.0.1:8000",
        help="Modifie si l’API est déployée (Render, Railway, etc.)"
    )
with colB:
    st.markdown(f"<span class='badge badge-url'>BASE</span> <span class='small'>{api_url}</span>", unsafe_allow_html=True)

st.divider()

# ---------- Endpoints ----------
st.header("📘 Endpoints disponibles")
st.markdown(
    """
- <span class='badge badge-get'>GET</span> **`/status`** — Vérifie la santé du service  
- <span class='badge badge-get'>GET</span> **`/last_update`** — Donne la dernière date de réception DPE  
- <span class='badge badge-get'>GET</span> **`/predict_sample`** — Prédiction rapide avec paramètres URL  
- <span class='badge badge-post'>POST</span> **`/predict_all`** — Prédiction complète (DPE + consommation)
""",
    unsafe_allow_html=True,
)
st.markdown(f"**Swagger** : [{api_url}/docs]({api_url}/docs) — **Redoc** : [{api_url}/redoc]({api_url}/redoc)")

st.divider()

# ---------- Schéma d'entrée POST ----------
st.header("📋 Schéma des champs attendus (POST /predict_all)")
schema_df = pd.DataFrame({
    "Champ": [
        "annee_construction","surface_habitable_logement","type_batiment","classe_inertie_batiment",
        "qualite_isolation_murs","qualite_isolation_menuiseries","classe_altitude","logement_traversant",
        "type_energie_principale_chauffage","periode_construction","energie_chauffage","zone_climatique"
    ],
    "Type": [
        "int","float","str","str","str","str","str","str","str","str","str","str"
    ],
    "Valeurs possibles": [
        "1990, 2005…","80, 120…","appartement / maison","Lourde, Légère, Moyenne, Très lourde",
        "bonne, moyenne, insuffisante, très bonne","bonne, moyenne, insuffisante, très bonne",
        "400-800m, Non affecté, inférieur à 400m, supérieur à 800m","oui / non",
        "Électricité, Gaz naturel, Bois – Bûches, etc.","Avant 1948, 1989-2000, 2006-2012",
        "Électricité, Gaz, Fioul, Bois","H1, H2, H3"
    ]
})
st.dataframe(schema_df, use_container_width=True, hide_index=True)
st.divider()

# ---------- Exemple JSON ----------
example_payload = {
    "annee_construction": 1990,
    "surface_habitable_logement": 80,
    "type_batiment": "appartement",
    "classe_inertie_batiment": "Lourde",
    "qualite_isolation_murs": "bonne",
    "qualite_isolation_menuiseries": "bonne",
    "classe_altitude": "400-800m",
    "logement_traversant": "oui",
    "type_energie_principale_chauffage": "Bois – Bûches",
    "periode_construction": "Avant 1948",
    "energie_chauffage": "Électricité",
    "zone_climatique": "H1"
}
st.subheader("🧾 Exemple de corps JSON (POST)")
st.code(json.dumps(example_payload, ensure_ascii=False, indent=2), language="json")
st.divider()

# ---------- Onglets principaux ----------
st.header("🧪 Outil de Requête interactif")

tab_predict, tab_status, tab_extra = st.tabs([
    "🔮 Prédire (POST /predict_all)",
    "📡 Statut (GET /status)",
    "🌐 Autres endpoints (GET)"
])

# ---- Tab 1 : Prédiction POST ----
with tab_predict:
    with st.form("predict_form"):
        st.markdown("Remplissez les champs pour exécuter une prédiction complète.")
        col1, col2 = st.columns(2)
        with col1:
            annee_construction = st.number_input("Année de construction", 1800, 2025, 1990)
            surface = st.number_input("Surface habitable (m²)", 10, 500, 80)
            type_batiment = st.selectbox("Type de bâtiment", ["appartement", "maison"])
            classe_inertie_batiment = st.selectbox("Classe d’inertie", ["Lourde","Légère","Moyenne","Très lourde"])
            qualite_isolation_murs = st.selectbox("Qualité isolation murs", ["bonne","insuffisante","moyenne","très bonne"])
        with col2:
            type_energie = st.selectbox("Énergie principale", [
                "Bois – Bûches","Gaz naturel","Fioul domestique","Électricité"
            ])
            qualite_isolation_menuiseries = st.selectbox("Qualité isolation menuiseries", ["bonne","insuffisante","moyenne","très bonne"])
            classe_altitude = st.selectbox("Classe altitude", ["400-800m","Non affecté","inférieur à 400m","supérieur à 800m"])
            logement_traversant_label = st.selectbox("Logement traversant", ["oui","non"])
            periode_construction = st.selectbox("Période de construction", ["Avant 1948","1948-1974","1989-2000","2006-2012"])
            energie_chauffage = st.selectbox("Énergie chauffage", ["Électricité","Gaz","Fioul","Bois"])
            zone_climatique = st.selectbox("Zone climatique", ["H1","H2","H3"])
        submitted = st.form_submit_button("🚀 Lancer la prédiction")

    if submitted:
        payload = {
            "annee_construction": int(annee_construction),
            "surface_habitable_logement": float(surface),
            "type_batiment": type_batiment,
            "classe_inertie_batiment": classe_inertie_batiment,
            "qualite_isolation_murs": qualite_isolation_murs,
            "qualite_isolation_menuiseries": qualite_isolation_menuiseries,
            "classe_altitude": classe_altitude,
            "logement_traversant": logement_traversant_label,
            "type_energie_principale_chauffage": type_energie,
            "periode_construction": periode_construction,
            "energie_chauffage": energie_chauffage,
            "zone_climatique": zone_climatique
        }

        col_req, col_resp = st.columns(2)
        with col_req:
            st.markdown("**Requête JSON envoyée :**")
            st.code(json.dumps(payload, ensure_ascii=False, indent=2), language="json")

        try:
            t0 = time.perf_counter()
            r = requests.post(f"{api_url}/predict_all", json=payload, timeout=60)
            dt = time.perf_counter() - t0
            with col_resp:
                if r.status_code == 200:
                    data = r.json()
                    st.success(f"✅ 200 OK — {dt:.3f}s")
                    st.json(data)
                    colM1, colM2 = st.columns(2)
                    with colM1: st.metric("🏠 DPE", data.get("DPE", "—"))
                    with colM2: st.metric("⚡ Consommation", f"{data.get('Conso_kWh_m2','—')} kWh/m²/an")
                else:
                    st.error(f"Erreur {r.status_code}")
                    st.code(r.text)
        except Exception as e:
            st.error(f"Erreur API : {e}")

# ---- Tab 2 : Statut ----
with tab_status:
    st.markdown("Test de santé du service et chargement des modèles.")
    if st.button("📡 GET /status"):
        try:
            t0 = time.perf_counter()
            r = requests.get(f"{api_url}/status", timeout=30)
            dt = time.perf_counter() - t0
            if r.status_code == 200:
                st.success(f"✅ 200 OK — {dt:.3f}s")
                st.json(r.json())
            else:
                st.error(f"Erreur {r.status_code}")
                st.code(r.text)
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")

# ---- Tab 3 : Autres endpoints ----
with tab_extra:
    st.subheader("🗓️ GET /last_update")
    st.caption("Retourne la date de réception DPE la plus récente.")
    if st.button("🔁 Exécuter /last_update"):
        try:
            r = requests.get(f"{api_url}/last_update", timeout=30)
            if r.status_code == 200:
                st.success("✅ Succès")
                st.json(r.json())
            else:
                st.error(f"Erreur {r.status_code}")
                st.code(r.text)
        except Exception as e:
            st.error(f"Erreur GET /last_update : {e}")

    st.markdown("---")
    st.subheader("⚡ GET /predict_sample")
    st.caption("Prédiction rapide via paramètres URL (pas de corps JSON).")
    col1, col2 = st.columns(2)
    with col1:
        annee_construction = st.number_input("Année (GET)", 1800, 2025, 1990)
        surface = st.number_input("Surface (m², GET)", 10, 500, 80)
        type_batiment = st.selectbox("Type bâtiment (GET)", ["maison", "appartement"])
    with col2:
        energie = st.selectbox("Énergie principale (GET)", ["Électricité", "Gaz naturel", "Fioul domestique", "Bois – Bûches"])

    if st.button("🚀 Lancer /predict_sample"):
        try:
            url = (
                f"{api_url}/predict_sample?"
                f"annee_construction={annee_construction}&"
                f"surface_habitable_logement={surface}&"
                f"type_batiment={type_batiment}&"
                f"type_energie_principale_chauffage={energie.replace(' ', '%20')}"
            )
            r = requests.get(url, timeout=60)
            st.markdown(f"**URL :** `{url}`")
            if r.status_code == 200:
                st.success("✅ Succès")
                st.json(r.json())
            else:
                st.error(f"Erreur {r.status_code}")
                st.code(r.text)
        except Exception as e:
            st.error(f"Erreur /predict_sample : {e}")

# ---------- Note pédagogique ----------
st.divider()
st.markdown("""
### 🧭 Méthodes HTTP — Petit rappel

| Méthode | Rôle | Exemple d’usage |
|----------|------|-----------------|
| **GET** | Lecture / Consultation sans effet | `/status`, `/last_update`, `/predict_sample` |
| **POST** | Envoi de données pour calcul ou prédiction | `/predict_all` |

""")
