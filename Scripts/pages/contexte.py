import streamlit as st
import pandas as pd

def show():
    st.markdown('<p class="section-title"> Contexte et Exploration des Données</p>', unsafe_allow_html=True)
    
    # Bloc d'introduction
    st.markdown("""
    <div class="modern-card">
        <h3>ℹ️ À propos des données</h3>
        <p>Les données présentées ici concernent la performance énergétique des logements en France, 
        récupérées depuis le site officiel <a href='https://www.data.gouv.fr' target='_blank'>data.gouv.fr</a>.</p>
        <p>Vous pouvez explorer et filtrer ces données directement depuis cette interface.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    st.markdown('<p class="section-title"> Diagnostic de Performance Énergétique</p>', unsafe_allow_html=True)
        
    # --- Cartes d'information ---
    col1, col2 = st.columns([3, 2])
    with col1:
            st.markdown("""
            <div class="modern-card">
                <h3>💡 Qu'est-ce que le DPE ?</h3>
                <p>Le DPE évalue la performance énergétique d'un logement en mesurant sa consommation d'énergie 
                et son impact sur les émissions de gaz à effet de serre. C'est un outil essentiel pour la transition énergétique.</p>
            </div>
            """, unsafe_allow_html=True)
        
    with col2:
            st.markdown("""
            <div class="modern-card">
                <h3> Classes Énergétiques</h3>
                <span class="dpe-badge dpe-a">A</span> <span class="dpe-badge dpe-b">B</span>
                <span class="dpe-badge dpe-c">C</span> <span class="dpe-badge dpe-d">D</span><br>
                <span class="dpe-badge dpe-e">E</span> <span class="dpe-badge dpe-f">F</span>
                <span class="dpe-badge dpe-g">G</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Chargement du CSV
    df = pd.read_csv("data/enedis_69.csv", sep=';', encoding='utf-8')
    
    
    st.markdown('<p class="section-title"> Exploration des données</p>', unsafe_allow_html=True)
    
    # Encadré filtres déroulé par défaut
    with st.expander("🎛️ Filtres", expanded=True):
        col_to_filter = st.selectbox("Choisissez la colonne à filtrer", df.columns)
        
        filtered_df = df.copy()
        
        if df[col_to_filter].dtype == "object":
            unique_vals = df[col_to_filter].dropna().unique().tolist()
            selected_vals = st.multiselect(f"Valeurs de {col_to_filter} à afficher", unique_vals)
            
            if selected_vals:
                filtered_df = filtered_df[filtered_df[col_to_filter].isin(selected_vals)]
            else:
                st.warning("⚠️ Veuillez sélectionner la valeur souhaitée pour votre filtre")
                filtered_df = pd.DataFrame()
        
        elif pd.api.types.is_numeric_dtype(df[col_to_filter]):
            min_val = float(df[col_to_filter].min())
            max_val = float(df[col_to_filter].max())
            if min_val < max_val:
                selected_range = st.slider(f"Plage de {col_to_filter}", min_val, max_val, (min_val, max_val))
                filtered_df = filtered_df[(filtered_df[col_to_filter] >= selected_range[0]) & (filtered_df[col_to_filter] <= selected_range[1])]
            else:
                st.write(f"{col_to_filter} : {min_val}")
    
    st.markdown("---")
    
    # Affichage de la table filtrée
    if not filtered_df.empty:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{len(filtered_df)} lignes** correspondent aux filtres sélectionnés")
        with col2:
            # Bouton pour télécharger les données filtrées
            csv = filtered_df.to_csv(index=False, sep=';').encode('utf-8')
            st.download_button(
                label="📥 Télécharger CSV",
                data=csv,
                file_name='dpe_filtered.csv',
                mime='text/csv'
            )
        
        n_rows = st.number_input(
            "Nombre de lignes à afficher",
            min_value=1,
            max_value=len(filtered_df),
            value=min(10, len(filtered_df))
        )
        st.dataframe(filtered_df.head(n_rows), use_container_width=True)
    else:
        st.info("ℹ️ Aucune donnée à afficher pour ce filtre.")
    
    st.markdown("---")
    
    # Bloc pédagogique
    st.markdown("""
    <div class="modern-card">
        <h3>💡 Guide d'utilisation</h3>
        <ul>
            <li><strong>Explorer</strong> les données DPE pour différents types de logements et régions</li>
            <li><strong>Filtrer</strong> selon la colonne de votre choix et les valeurs associées</li>
            <li><strong>Visualiser</strong> la table qui se met à jour automatiquement</li>
            <li><strong>Télécharger</strong> les données filtrées au format CSV</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
