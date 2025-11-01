# scripts/app/pages/2_Analyse_et_visualisation.py
import streamlit as st
import pandas as pd
import plotly.express as px
from app.utils.data_loader import load_data

# ======================================================
# CONFIGURATION DE LA PAGE
# ======================================================
st.set_page_config(page_title="📊 Analyse et visualisation", layout="wide")
st.title("📊 Analyse et visualisation des données DPE")

# ======================================================
# CHARGEMENT DES DONNÉES
# ======================================================
df = load_data()

# ======================================================
# LISTE UNIFIÉE DES COLONNES PAR TYPE DE GRAPHIQUE
# ======================================================
GRAPHIC_COLUMNS = {
    "Histogramme / Barres empilées": {
        "x": [
            "periode_construction","etiquette_dpe", "Logement","nom_commune_ban",
            "annee_construction","annee_reception_DPE","type_batiment","classe_altitude","zone_climatique",
            "classe_inertie_batiment","etiquette_ges","surface_habitable_logement"
            ,"indicateur_confort_ete","logement_traversant","isolation_toiture","qualite_isolation_enveloppe",
            "qualite_isolation_murs","qualite_isolation_menuiseries","type_energie_principale_chauffage","type_energie_principale_ecs"
        ],
        "y": [],
        "color": [
            "type_batiment","code_postal_ban","annee_reception_DPE","periode_construction",
            "Logement","classe_altitude","classe_inertie_batiment","etiquette_dpe",
            "etiquette_ges","indicateur_confort_ete","logement_traversant","isolation_toiture",
            "qualite_isolation_enveloppe","qualite_isolation_murs","qualite_isolation_menuiseries",
            "type_energie_principale_chauffage","type_energie_principale_ecs"
        ],
    },
    "Boxplot": {
        "x": [
            "conso_5_usages_par_m2_ef","annee_construction", "conso_5_usages_ef", "conso_chauffage_ef", 
            "conso_ecs_ef", "emission_ges_5_usages", "emission_ges_5_usages_par_m2", "surface_habitable_logement", 
            "ubat_w_par_m2_k","cout_total_5_usages", "cout_chauffage", "cout_ecs",
            "cout_refroidissement", "cout_eclairage", "cout_auxiliaires"
        ],
        "y": [],
        "color": [
            "Logement","annee_reception_DPE","periode_construction", "type_batiment", "zone_climatique",
            "classe_altitude","classe_inertie_batiment", "etiquette_dpe", "etiquette_ges",
            "type_energie_principale_chauffage", "type_energie_principale_ecs"
        ],
    },
    "Nuage de points (Scatterplot)": {
        "x": [
            "conso_5_usages_ef","conso_chauffage_ef","conso_ecs_ef",
            "conso_5_usages_par_m2_ef","emission_ges_5_usages_par_m2",
            "surface_habitable_logement","ubat_w_par_m2_k","cout_total_5_usages", "cout_chauffage", "cout_ecs", 
            "cout_refroidissement", "cout_eclairage", "cout_auxiliaires"  
        ],
        "y": [
            "conso_5_usages_ef","conso_5_usages_par_m2_ef","emission_ges_5_usages_par_m2",
            "surface_habitable_logement","ubat_w_par_m2_k","cout_total_5_usages"
             "cout_chauffage", "cout_ecs","cout_refroidissement",  "cout_eclairage", "cout_auxiliaires"
        ],
        "color": [
            "periode_construction","type_batiment","zone_climatique","classe_altitude"
            "etiquette_dpe","etiquette_ges","annee_reception_DPE","Logement",
            "type_energie_principale_chauffage",  "type_energie_principale_ecs",
        ],
    },
    "Camembert (Piechart)": {
        "x": [
            "etiquette_dpe","periode_construction","Logement","code_postal_ban","nom_commune_ban",
            "annee_construction","annee_reception_DPE","type_batiment","classe_altitude","zone_climatique",
            "classe_inertie_batiment","etiquette_ges","indicateur_confort_ete",
            "logement_traversant","isolation_toiture","qualite_isolation_enveloppe",
            "qualite_isolation_murs","qualite_isolation_menuiseries",
            "type_energie_principale_chauffage","type_energie_principale_ecs"
        ],
        "y": [],
        "color": [],
    },
}

# ======================================================
# PANNEAU LATÉRAL UNIFIÉ
# ======================================================
st.sidebar.header("⚙️ Paramètres du graphique")

chart_type = st.sidebar.selectbox(
    "Type de graphique",
    list(GRAPHIC_COLUMNS.keys())
)

options = GRAPHIC_COLUMNS[chart_type]

x_var = st.sidebar.selectbox("Variable principale (X ou variable à analyser)", options=options.get("x", []))
y_var = None
if options.get("y"):
    y_var = st.sidebar.selectbox("Variable en ordonnée (Y)", options=options.get("y", []))

color_var = st.sidebar.selectbox("Variable de regroupement", options=[None] + options.get("color", []))

# ======================================================
# STATISTIQUES DE BASE
# ======================================================
st.subheader("📊 Statistiques descriptives")

with st.expander("Afficher les statistiques de base", expanded=False):
    styled_df = (
        df.describe()
        .transpose()
        .style.set_table_styles([
            {"selector": "th", "props": [("text-align", "center")]},
            {"selector": "td", "props": [("text-align", "right")]},
        ])
        .set_properties(**{
            "border": "1px solid #ddd",
            "padding": "6px",
        })
    )
    st.dataframe(styled_df, use_container_width=True)

# ======================================================
# VISUALISATIONS INTERACTIVES
# ======================================================
st.subheader("📉 Visualisation interactive")

fig = None

# --- Histogramme / Barres empilées ---
if chart_type == "Histogramme / Barres empilées":
    fig = px.histogram(
        df,
        x=x_var,
        color=color_var if color_var else None,
        nbins=50,
        title=f"Histogramme / Barres empilées de {x_var}" + (f" par {color_var}" if color_var else ""),
    )

# --- Boxplot unifié (analyse univariée) ---
elif chart_type == "Boxplot":
    fig = px.box(
        df,
        y=x_var,
        color=color_var if color_var else None,
        points=False,
        title=f"Distribution de {x_var}" + (f" par {color_var}" if color_var else ""),
    )

# --- Nuage de points ---
elif chart_type == "Nuage de points (Scatterplot)":
    fig = px.scatter(
        df,
        x=x_var,
        y=y_var,
        color=color_var if color_var else None,
        hover_data=[x_var, y_var],
        title=f"Nuage de points : {x_var} vs {y_var}",
    )

# --- Camembert ---
elif chart_type == "Camembert (Piechart)":
    fig = px.pie(
        df,
        names=x_var,
        color=color_var if color_var else None,
        title=f"Répartition de {x_var}",
    )

# --- Affichage du graphique ---
if fig:
    fig.update_layout(
        plot_bgcolor="white",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# CORRÉLATION AUTOMATIQUE (SI PERTINENTE)
# ======================================================
if (
    chart_type == "Nuage de points (Scatterplot)"
    and y_var
    and x_var in df.columns
    and pd.api.types.is_numeric_dtype(df[x_var])
    and pd.api.types.is_numeric_dtype(df[y_var])
):
    corr_value = df[[x_var, y_var]].corr().iloc[0, 1]
    st.info(f"📈 Corrélation entre **{x_var}** et **{y_var}** : {corr_value:.3f}")
