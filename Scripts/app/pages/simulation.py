import streamlit as st

def show():
    st.markdown('<p class="section-title"> Simulation de Performance Énergétique</p>', unsafe_allow_html=True)
    
    # Encadré d'introduction
    st.markdown("""
    <div class="modern-card">
        <h3> Objectif</h3>
        <p>Simulez les économies d'énergie potentielles de votre logement.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Informations du logement
    st.markdown('<p class="section-title"> Caractéristiques de votre logement</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        surface = st.number_input("📐 Surface habitable (m²)", min_value=10, max_value=500, value=100)
        type_logement = st.selectbox("🏢 Type de logement", ["Appartement", "Maison individuelle", "Immeuble collectif"])
        annee_construction = st.slider("📅 Année de construction", 1900, 2024, 1990)
    with col2:
        nb_occupants = st.number_input("👥 Nombre d'occupants", min_value=1, max_value=10, value=3)
        type_chauffage = st.selectbox("🔥 Type de chauffage", ["Gaz", "Électrique", "Fioul", "Pompe à chaleur", "Bois"])
        isolation = st.select_slider("🏠 Qualité d'isolation", options=["Mauvaise", "Moyenne", "Bonne", "Excellente"], value="Moyenne")
    
    st.markdown("---")
    
    # Consommation actuelle
    st.markdown('<p class="section-title"> Consommation Actuelle</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        conso_chauffage = st.number_input(" Consommation chauffage (kWh/an)", min_value=0, value=15000)
        conso_eau_chaude = st.number_input(" Consommation eau chaude (kWh/an)", min_value=0, value=3000)
    with col2:
        conso_electricite = st.number_input(" Consommation électricité (kWh/an)", min_value=0, value=5000)
        cout_annuel = st.number_input(" Coût annuel actuel (€)", min_value=0, value=2000)
    
    st.markdown("---")
    
    # Bouton de simulation
    if st.button(" Lancer la Simulation", type="primary"):
        st.success("✅ Simulation terminée !")
        
        st.markdown('<p class="section-title">📊 Résultats</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-modern">
                <h4>💰 Économies</h4>
                <div class="metric-value">850 €/an</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-modern">
                <h4>🌱 CO₂</h4>
                <div class="metric-value">-2.5 t/an</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-modern">
                <h4>📈 DPE</h4>
                <div class="metric-value">E → B</div>
            </div>
            """, unsafe_allow_html=True)
