import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
from pyproj import Transformer
import os

# ====================================================
#  Chargement des données
# ====================================================
@st.cache_data(ttl=3600)
def load_data():
    """Charge et prépare les données nettoyées"""
    csv_path = r"C:\Users\ychen\OneDrive\Documents\GitHub\SISE_Enedis\data\donnees_dpe_69_clean.csv"
    try:
        df = pd.read_csv(csv_path, sep=',', encoding='utf-8', low_memory=False)
        st.success(f"✅ Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du fichier : {e}")
        return pd.DataFrame()
    return df

# ====================================================
#  Données cartographiques
# ====================================================
@st.cache_data(ttl=3600)
def prepare_map_data(df):
    """Prépare les données cartographiques"""
    transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True)
    df_map = df.dropna(subset=['coordonnee_cartographique_x_ban', 'coordonnee_cartographique_y_ban']).copy()
    df_map['lon'], df_map['lat'] = transformer.transform(
        df_map['coordonnee_cartographique_x_ban'].values,
        df_map['coordonnee_cartographique_y_ban'].values
    )
    df_map = df_map[(df_map['lat'].between(41, 51)) & (df_map['lon'].between(-5, 10))]
    if len(df_map) > 50_000:
        df_map = df_map.sample(50_000, random_state=42)
    return df_map

# ====================================================
#  Interface principale
# ====================================================
def show():
    with st.spinner('🔄 Chargement des données...'):
        df = load_data()
    if df.empty:
        st.stop()

    tab_stats, tab_graphs, tab_map = st.tabs([" Statistiques", " Graphiques", " Cartographie"])

    # === ONGLET 1 : STATISTIQUES ===
    with tab_stats:
        st.markdown('<p class="section-title"> Filtrer les données</p>', unsafe_allow_html=True)

        # --- FILTRES ---
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_codes_postaux = st.multiselect(" Code postal", 
                options=sorted(df['code_postal_ban'].dropna().unique()), key="cp_stats")
        with col2:
            selected_types_batiment = st.multiselect(" Type de bâtiment", 
                options=sorted(df['type_batiment'].dropna().unique()), key="bat_stats")
        with col3:
            selected_periodes = st.multiselect(" Période construction", 
                options=sorted(df['periode_construction'].dropna().unique()), key="per_stats")

        col4, col5 = st.columns(2)
        with col4:
            selected_types_energie = st.multiselect(" Énergie chauffage", 
                options=sorted(df['type_energie_principale_chauffage'].dropna().unique()), key="ener_stats")
        with col5:
            selected_types_energie_ecs = st.multiselect(" Énergie ECS", 
                options=sorted(df['type_energie_principale_ecs'].dropna().unique()), key="ecs_stats")

        min_surface = int(df['surface_habitable_logement'].min())
        max_surface = int(df['surface_habitable_logement'].max())
        selected_surface = st.slider(" Surface habitable (m²)", min_value=min_surface, 
            max_value=max_surface, value=(min_surface, max_surface), key="surf_stats")

        # --- APPLICATION DES FILTRES ---
        filtered_df = df.copy()
        if selected_codes_postaux:
            filtered_df = filtered_df[filtered_df['code_postal_ban'].isin(selected_codes_postaux)]
        if selected_types_batiment:
            filtered_df = filtered_df[filtered_df['type_batiment'].isin(selected_types_batiment)]
        if selected_types_energie:
            filtered_df = filtered_df[filtered_df['type_energie_principale_chauffage'].isin(selected_types_energie)]
        if selected_types_energie_ecs:
            filtered_df = filtered_df[filtered_df['type_energie_principale_ecs'].isin(selected_types_energie_ecs)]
        if selected_periodes:
            filtered_df = filtered_df[filtered_df['periode_construction'].isin(selected_periodes)]
        filtered_df = filtered_df[
            (filtered_df['surface_habitable_logement'] >= selected_surface[0]) &
            (filtered_df['surface_habitable_logement'] <= selected_surface[1])
        ]

        st.markdown("---")
        st.markdown('<p class="section-title"> Résultats</p>', unsafe_allow_html=True)

        conso_cols = {
            " Consommation totale": ("conso_5_usages_ef", "kWh/an"),
            " Consommation chauffage": ("conso_chauffage_ef", "kWh/an"),
            " Consommation eau chaude": ("conso_ecs_ef", "kWh/an")
        }

        if filtered_df.empty:
            st.warning("⚠️ Aucune donnée ne correspond aux filtres sélectionnés.")
        else:
            cols = st.columns(3)
            for col, (label, (col_name, unit)) in zip(cols, conso_cols.items()):
                if col_name in filtered_df.columns and not filtered_df[col_name].dropna().empty:
                    mean_val = filtered_df[col_name].mean()
                    std_val = filtered_df[col_name].std()
                    min_val = filtered_df[col_name].min()
                    max_val = filtered_df[col_name].max()
                    col.markdown(f"""
                    <div class="metric-modern">
                        <h4>{label}</h4>
                        <div style="font-size: 0.9rem; color: #666; margin-bottom: 8px; font-weight: 600;">Moyenne</div>
                        <div class="metric-value">{mean_val:,.0f} {unit}</div>
                        <div class="metric-detail"> Écart-type: {std_val:,.0f} {unit}</div>
                        <div class="metric-detail"> Min: {min_val:,.0f} {unit} |  Max: {max_val:,.0f} {unit}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # === ONGLET 2 : GRAPHIQUES ===
    with tab_graphs:
        st.markdown('<p class="section-title"> Visualisation graphique interactive</p>', unsafe_allow_html=True)

        colonnes_disponibles = [
            "annee_construction", "type_batiment", "surface_habitable_logement",
            "etiquette_dpe", "etiquette_ges",
            "conso_5_usages_par_m2_ep", "conso_5_usages_ef",
            "emission_ges_5_usages_par_m2", "conso_chauffage_ef",
            "conso_ecs_ef", "type_energie_principale_chauffage",
            "type_energie_principale_ecs", "cout_total_5_usages", 
            "cout_chauffage", "cout_ecs", "ubat_w_par_m2_k",
            "qualite_isolation_enveloppe", "qualite_isolation_menuiseries",
            "qualite_isolation_murs", "isolation_toiture", "indicateur_confort_ete",
            "logement_traversant"
        ]

        noms_affiches = {
            "annee_construction": "Année de construction",
            "type_batiment": "Type de bâtiment",
            "surface_habitable_logement": "Surface habitable (m²)",
            "etiquette_dpe": "Étiquette DPE",
            "etiquette_ges": "Étiquette GES",
            "conso_5_usages_par_m2_ep": "Conso énergie primaire (kWh/m².an)",
            "conso_5_usages_ef": "Conso totale énergie finale (kWh/an)",
            "emission_ges_5_usages_par_m2": "Émissions CO₂ (kgCO₂/m².an)",
            "conso_chauffage_ef": "Conso chauffage (kWh/an)",
            "conso_ecs_ef": "Conso eau chaude (kWh/an)",
            "type_energie_principale_chauffage": "Type d'énergie principale chauffage",
            "type_energie_principale_ecs": "Type d'énergie principale ECS",
            "cout_total_5_usages": "Coût total énergie (€)",
            "cout_chauffage": "Coût chauffage (€)",
            "cout_ecs": "Coût ECS (€)",
            "ubat_w_par_m2_k": "Déperdition thermique (Ubat W/m².K)",
            "qualite_isolation_enveloppe": "Qualité isolation enveloppe",
            "qualite_isolation_menuiseries": "Qualité isolation menuiseries",
            "qualite_isolation_murs": "Qualité isolation murs",
            "isolation_toiture": "Isolation toiture",
            "indicateur_confort_ete": "Indicateur confort été",
            "logement_traversant": "Logement traversant"
        }

        palette = ["#097536", "#4CAF50", "#81C784", "#A5D6A7", "#C8E6C9"]

        type_graphique = st.selectbox(" Type de graphique", ["Histogramme", "Nuage de points", "Boxplot", "Diagramme circulaire"])

        if type_graphique == "Nuage de points":
            valeur_x = st.selectbox("Axe X", options=colonnes_disponibles, format_func=lambda x: noms_affiches.get(x, x))
            colonnes_y = [c for c in colonnes_disponibles if c != valeur_x]
            valeur_y = st.selectbox("Axe Y", options=colonnes_y, format_func=lambda x: noms_affiches.get(x, x))
        else:
            valeur_x = st.selectbox("Variable", options=colonnes_disponibles, format_func=lambda x: noms_affiches.get(x, x))
            valeur_y = None

        if valeur_x:
            data = df[[valeur_x]].dropna() if valeur_y is None else df[[valeur_x, valeur_y]].dropna()
            if len(data) > 100_000:
                data = data.sample(100_000, random_state=42)

            if not data.empty:
                if type_graphique == "Histogramme":
                    fig = px.histogram(data, x=valeur_x, nbins=30, color_discrete_sequence=palette)
                elif type_graphique == "Nuage de points":
                    fig = px.scatter(data, x=valeur_x, y=valeur_y, opacity=0.5, color_discrete_sequence=palette)
                elif type_graphique == "Boxplot":
                    fig = px.box(data, y=valeur_x, color_discrete_sequence=palette)
                elif type_graphique == "Diagramme circulaire":
                    counts = data[valeur_x].value_counts().head(8).reset_index()
                    counts.columns = [valeur_x, 'Count']
                    fig = px.pie(counts, names=valeur_x, values='Count', color_discrete_sequence=palette)

                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#094c2e'),
                    margin=dict(l=20, r=20, t=50, b=20),
                    title_x=0.5,
                    title_font=dict(size=18, color='#097536')
                )
                st.plotly_chart(fig, use_container_width=True)

    # === ONGLET 3 : CARTOGRAPHIE ===
    with tab_map:
        st.markdown('<p class="section-title"> Cartographie des logements DPE</p>', unsafe_allow_html=True)

        with st.spinner(' Préparation de la carte...'):
            df_map = prepare_map_data(df)

        etiquettes_dispo = sorted(df_map['etiquette_dpe'].dropna().unique())
        selected_etiquettes = st.multiselect("🏷️ Filtrer par classe énergétique :", options=etiquettes_dispo, default=etiquettes_dispo[:3])

        if selected_etiquettes:
            df_filtered = df_map[df_map['etiquette_dpe'].isin(selected_etiquettes)]
        else:
            df_filtered = df_map.head(10000)

        color_map = {"A": "#007f00", "B": "#4CAF50", "C": "#CDDC39", "D": "#FFEB3B", "E": "#FFC107", "F": "#FF5722", "G": "#B71C1C"}

        m = folium.Map(location=[45.75, 4.85], zoom_start=9, tiles="cartodb positron")
        for _, row in df_filtered.iterrows():
            dpe = str(row.get('etiquette_dpe', 'N/A'))
            tooltip_html = f"""
                <b>🏷️ Étiquette DPE :</b> {dpe}<br>
                <b>🏢 Type bâtiment :</b> {row.get('type_batiment', 'N/A')}<br>
                <b>📐 Surface :</b> {row.get('surface_habitable_logement', 'N/A')} m²<br>
                <b>📅 Année construction :</b> {row.get('annee_construction', 'N/A')}<br>
                <b>🏘️ Commune :</b> {row.get('nom_commune_ban', 'N/A')}<br>
                <b>⚡ Conso totale :</b> {row.get('conso_5_usages_ef', 'N/A')} kWh/an
            """
            folium.CircleMarker(location=[row['lat'], row['lon']], radius=4, color=color_map.get(dpe, "gray"), fill=True, fill_opacity=0.7, tooltip=tooltip_html).add_to(m)

        st_folium(m, width=None, height=600, returned_objects=[])