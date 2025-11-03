# scripts/app/pages/1_Exploration.py
import streamlit as st
import pandas as pd
import plotly.express as px
from app.utils.data_loader import load_data
from app.utils.ui_style import apply_greentech_style

# ======================================================
# CONFIGURATION DE LA PAGE
# ======================================================
st.set_page_config(page_title="🔍 Exploration des données", layout="wide")
apply_greentech_style()
st.title("🔍 Exploration des données DPE")
# ======================================================
# 🔁 Rafraîchissement des données ADEME
# ======================================================

import requests

API_URL = "http://127.0.0.1:8000"  # à adapter selon ton déploiement local ou Render

# --- Lecture de la dernière mise à jour ---
try:
    r = requests.get(f"{API_URL}/last_update", timeout=15)
    if r.status_code == 200:
        last_date = r.json().get("last_update", "Non disponible")
    else:
        last_date = "Non disponible"
except Exception:
    last_date = "Non disponible"

with st.container(border=True):
    st.markdown("### 🗓️ Données ADEME locales")
    st.markdown(f"**Dernière mise à jour enregistrée :** `{last_date}`")

    if st.button("🔁 Rafraîchir les données depuis l’ADEME"):
        with st.spinner("⏳ Mise à jour en cours... (cela peut prendre quelques minutes)"):
            try:
                res = requests.post(f"{API_URL}/refresh_data", timeout=600)
                if res.status_code == 200:
                    payload = res.json()
                    if payload["status"] == "ok":
                        st.success(
                            f"✅ {payload['new_rows']} nouvelles lignes ajoutées "
                            f"(dernière date : {payload['updated_until']})."
                        )
                        st.rerun()
                    else:
                        st.info("ℹ️ Aucune nouvelle donnée trouvée (déjà à jour).")
                else:
                    st.error(f"Erreur {res.status_code}")
                    st.code(res.text)
            except Exception as e:
                st.error(f"❌ Erreur de connexion à l’API : {e}")

# ======================================================
# CHARGEMENT DES DONNÉES
# ======================================================
df = load_data()
if "date_reception_dpe" in df.columns:
    df["date_reception_dpe"] = pd.to_datetime(df["date_reception_dpe"], errors="coerce").dt.date
    df = df.sort_values("date_reception_dpe", ascending=False)


# ======================================================
# SECTION FILTRES
# ======================================================
with st.expander("🎚️ Filtres de sélection", expanded=True):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        codes = st.multiselect(
            "Code postal",
            options=sorted(df["code_postal_ban"].dropna().unique()),
            default=None
        )

    with col2:
        types_b = st.multiselect(
            "Type de bâtiment",
            options=sorted(df["type_batiment"].dropna().unique()),
            default=None
        )

    with col3:
        periodes = st.multiselect(
            "Période de construction",
            options=sorted(df["periode_construction"].dropna().unique()),
            default=None
        )

    with col4:
        energies = st.multiselect(
            "Énergie chauffage",
            options=sorted(df["type_energie_principale_chauffage"].dropna().unique()),
            default=None
        )

# ======================================================
# APPLICATION DES FILTRES
# ======================================================
filtered_df = df.copy()
if codes:
    filtered_df = filtered_df[filtered_df["code_postal_ban"].isin(codes)]
if types_b:
    filtered_df = filtered_df[filtered_df["type_batiment"].isin(types_b)]
if periodes:
    filtered_df = filtered_df[filtered_df["periode_construction"].isin(periodes)]
if energies:
    filtered_df = filtered_df[filtered_df["type_energie_principale_chauffage"].isin(energies)]

st.markdown(f"### 📊 Données filtrées : {filtered_df.shape[0]:,} lignes affichées")

# ======================================================
# AFFICHAGE DU TABLEAU AVEC PAGINATION ET FORMATAGE
# ======================================================
ROWS_PER_PAGE = 50
total_rows = len(filtered_df)
total_pages = max(1, (total_rows - 1) // ROWS_PER_PAGE + 1)

if "page_number" not in st.session_state:
    st.session_state.page_number = 1

col_prev, col_page, col_next = st.columns([1, 2, 1])
with col_prev:
    if st.button("◀ Précédent", use_container_width=True) and st.session_state.page_number > 1:
        st.session_state.page_number -= 1
with col_next:
    if st.button("Suivant ▶", use_container_width=True) and st.session_state.page_number < total_pages:
        st.session_state.page_number += 1
with col_page:
    st.markdown(
        f"<div style='text-align:center;'>Page {st.session_state.page_number} / {total_pages}</div>",
        unsafe_allow_html=True
    )

start_idx = (st.session_state.page_number - 1) * ROWS_PER_PAGE
end_idx = start_idx + ROWS_PER_PAGE
page_df = filtered_df.iloc[start_idx:end_idx]

# --- Formatage des valeurs (nombres sans séparateurs pour les entiers) ---
def format_values(val):
    if isinstance(val, (int, float)):
        if float(val).is_integer():
            return f"{int(val)}"
        else:
            return f"{val:,.2f}".replace(",", " ")
    return val

formatted_page = page_df.applymap(format_values)

st.dataframe(formatted_page, use_container_width=True)

# ======================================================
# STATISTIQUES SOMMAIRES
# ======================================================
st.subheader("📈 Statistiques principales")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Surface moyenne (m²)", round(filtered_df["surface_habitable_logement"].mean(), 2))
with col2:
    st.metric("Conso moyenne (kWh/m²)", round(filtered_df["conso_5_usages_par_m2_ef"].mean(), 2))
with col3:
    st.metric("Émissions moy. GES (kgCO₂/m²)", round(filtered_df["emission_ges_5_usages_par_m2"].mean(), 2))

# ======================================================
# VISUALISATIONS
# ======================================================
st.subheader("📉 Visualisations")

tab1, tab2 = st.tabs(["Répartition par étiquette DPE", "Surface vs Consommation énergétique"])

with tab1:
    possible_cols = ["etiquette_dpe", "classe_consommation_energie", "classe_consommation_energie_5_usages"]
    energy_col = next((c for c in possible_cols if c in filtered_df.columns), None)

    if energy_col:
        DPE_COLORS = {
            "A": "#007f00", "B": "#4CAF50", "C": "#CDDC39",
            "D": "#FFEB3B", "E": "#FFC107", "F": "#FF5722", "G": "#B71C1C",
        }

        fig = px.histogram(
            filtered_df,
            x=energy_col,
            color=energy_col,
            title="Distribution des classes énergétiques (DPE)",
            category_orders={energy_col: ["A", "B", "C", "D", "E", "F", "G"]},
            color_discrete_map=DPE_COLORS,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune colonne de classe énergétique trouvée.")

with tab2:
    fig2 = px.scatter(
        filtered_df,
        x="surface_habitable_logement",
        y="conso_5_usages_par_m2_ef",
        color="type_energie_principale_chauffage" if "type_energie_principale_chauffage" in filtered_df.columns else None,
        hover_data=["code_postal_ban", "periode_construction"],
        title="Surface vs Consommation énergétique",
    )
    st.plotly_chart(fig2, use_container_width=True)
