import streamlit as st
import pandas as pd

def show():
    st.markdown("## 📊 Contexte et Exploration des Données")
    
    # Bloc d'introduction
    st.markdown("""
    <div class="info-card">
        <h3>ℹ️ À propos des données</h3>
        <p>Les données présentées ici concernent la performance énergétique des logements en France, 
        récupérées depuis le site officiel <a href='https://www.data.gouv.fr' target='_blank'>data.gouv.fr</a>.</p>
        <p>Vous pouvez explorer et filtrer ces données directement depuis cette interface.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Chargement du CSV
    df = pd.read_csv("data/enedis_69.csv", sep=';', encoding='utf-8')
    
    st.markdown("### 🔍 Exploration des données")
    
    # Encadré filtres déroulé par défaut
    with st.expander("Filtres", expanded=True):
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
    
    # Affichage de la table filtrée
    if not filtered_df.empty:
        # Bouton pour télécharger les données filtrées
        csv = filtered_df.to_csv(index=False, sep=';').encode('utf-8')
        st.download_button(
            label="📥 Télécharger les données filtrées",
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
        st.info("Aucune donnée à afficher pour ce filtre.")
    
    st.markdown("---")
    
    # Bloc pédagogique
    st.markdown("""
    <div class="info-card">
        <h3>💡 Utilisation de cette section</h3>
        <ul>
            <li>Explorer les données DPE pour différents types de logements et régions</li>
            <li>Filtrer selon la colonne de votre choix et les valeurs associées</li>
            <li>La table affichée se met à jour automatiquement selon votre filtre</li>
            <li>Vous pouvez télécharger les données filtrées avec le bouton ci-dessus</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
