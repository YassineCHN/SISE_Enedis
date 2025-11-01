# scripts/app/pages/3_Cartographie.py
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from app.utils.data_loader import load_data

# ======================================================
# CONFIGURATION
# ======================================================
st.set_page_config(page_title="🗺️ Cartographie DPE", layout="wide")
st.title("🗺️ Cartographie interactive des logements DPE")

df = load_data()

# Vérification des colonnes nécessaires
if not {"latitude", "longitude"}.issubset(df.columns):
    st.error("❌ Les colonnes 'latitude' et 'longitude' sont manquantes dans le dataset.")
    st.stop()

# Nettoyage (suppression des coordonnées manquantes)
df = df.dropna(subset=["latitude", "longitude"])

# ======================================================
# FILTRES
# ======================================================
st.sidebar.header("🎚️ Filtres de la carte")

codes = st.sidebar.multiselect("Code postal", sorted(df["code_postal_ban"].dropna().unique()))
types_b = st.sidebar.multiselect("Type de bâtiment", sorted(df["type_batiment"].dropna().unique()))
etiquettes = st.sidebar.multiselect("Étiquette DPE", ["A","B","C","D","E","F","G"])

filtered_df = df.copy()
if codes:
    filtered_df = filtered_df[filtered_df["code_postal_ban"].isin(codes)]
if types_b:
    filtered_df = filtered_df[filtered_df["type_batiment"].isin(types_b)]
if etiquettes and "etiquette_dpe" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["etiquette_dpe"].isin(etiquettes)]

# ======================================================
# LIMITATION DES POINTS
# ======================================================
MAX_POINTS = 6000
if len(filtered_df) > MAX_POINTS:
    st.warning(f"Trop de points à afficher ({len(filtered_df):,}). Seuls {MAX_POINTS} seront utilisés.")
    filtered_df = filtered_df.sample(MAX_POINTS, random_state=42)

if filtered_df.empty:
    st.warning("Aucun logement ne correspond à ces filtres.")
    st.stop()

# ======================================================
# COULEURS DPE
# ======================================================
DPE_COLORS = {
    "A": "#007f00", "B": "#4CAF50", "C": "#CDDC39",
    "D": "#FFEB3B", "E": "#FFC107", "F": "#FF5722", "G": "#B71C1C"
}

# ======================================================
# CARTE FOLIUM
# ======================================================
center = [filtered_df["latitude"].mean(), filtered_df["longitude"].mean()]
m = folium.Map(location=center, zoom_start=8, tiles="CartoDB positron")

marker_cluster = MarkerCluster().add_to(m)

for _, row in filtered_df.iterrows():
    color = DPE_COLORS.get(row.get("etiquette_dpe", "N/A"), "#808080")
    popup = folium.Popup(html=f"""
        <b>Commune :</b> {row.get('nom_commune_ban', '')}<br>
        <b>Type :</b> {row.get('type_batiment', '')}<br>
        <b>DPE :</b> {row.get('etiquette_dpe', 'N/A')}<br>
        <b>Surface :</b> {row.get('surface_habitable_logement', '')} m²<br>
        <b>Conso (kWh/m²) :</b> {row.get('conso_5_usages_par_m2_ef', '')}
    """, max_width=250)

    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=4,
        color=color,
        fill=True,
        fill_opacity=0.8,
        popup=popup
    ).add_to(marker_cluster)

# ======================================================
# AFFICHAGE
# ======================================================
st.subheader(f"📍 {len(filtered_df)} logements affichés sur la carte")
st_folium(m, width=1300, height=700)
