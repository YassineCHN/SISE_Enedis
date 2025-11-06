# 📘 Documentation Fonctionnelle – GreenTech Solutions

## Présentation du projet

**GreenTech Solutions** est une application web interactive combinant **Streamlit** (interface utilisateur) et **FastAPI** (API de prédiction), déployée sur **Koyeb**.  
Elle permet d’explorer les données du **Diagnostic de Performance Énergétique (DPE)** (ADEME), d’analyser la consommation énergétique des logements et de **prédire la classe DPE et la consommation estimée** d’un logement.

**URL de déploiement :** [Application Streamlit sur Koyeb](https://appstreamlit.koyeb.app/)  
**Dépôt GitHub :** https://github.com/YassineCHN/SISE_Enedis

---

## Navigation et pages principales

### 🏠 Contexte
**Objectif** : Introduire le projet, son cadre (sobriété énergétique) et les jeux de données ADEME.  
**Utilisation** : Page d’accueil explicative.

---

### 📊 Exploration
**Objectif** : Explorer le dataset ADEME nettoyé pour la **Savoie (73)**.  
**Fonctionnalités** :
- Chargement du fichier `donnees_dpe_73_clean.csv`
- Filtres : code postal, type de bâtiment, période de construction, énergie de chauffage
- Rafraichir les données (interroge l'API de l'ADEME selon la dernière date_reception_dpe chargé)
- Statistiques principales sur le jeux de données (dynamique selon les filtres) : Surface moyenne, Conso moyenne, Emission moyenne
- Export : données filtrées en **CSV**

**Utilisation** : Choisir des filtres et explorer le jeux de données

---

### 📈 Analyse Statistique
**Objectif** : Étudier les relations entre caractéristiques des logements et performances énergétiques.  
**Fonctionnalités** :
- Statistiques principales des données numériques (téléchargeable en CSV) : count, mean, std, min, q1, q2, q3, max
- Différents types de visualisations (**Plotly**) : Histogramme/barres empilées, Boxplot, Scatterplot, Piechart
- Plusieurs possibilités de variables X (et Y pour les types de graphiques concernés) et possibilité d'utiliser une variable de regroupement
- Visualisations interactives (téléchargeable en png) : Zoomer et dézoomer sur le graphique, affichage d'étiquette en survol, subdiviser une partie du graphique

**Utilisation** : Identifier tendances globales et variables influentes. Choisir les filtres (sidebar) → visuels mis à jour en temps réel. Cliquer sur les graphiques pour intéragir.

---

### 🗺️ Cartographie
**Objectif** : Visualiser la répartition géographique des logements.  
**Fonctionnalités** :
- Carte **Folium** intégrée à Streamlit
- Conversion géographique **Lambert93 → WGS84**
- Filtres : étiquette DPE, code postal, type de bâtiment
- Navigation (zoom, clic) et **export image**

**Utilisation** : Explorer zones performantes vs énergivores.

---

### 🤖 Prédiction
**Objectif** : Simuler **classe DPE (A–G)** et **consommation (kWh/m²/an)**.  
**Formulaire** :
- Type (maison/appartement), surface, année de construction
- Énergie principale de chauffage, logement traversant (Oui/Non), Classe d'altitude 
- Qualité d’isolation des murs, qualité des menuiseries, qualité d'inertie

**Modèles** :
- **Classification DPE** : Random Forest Classifier  
- **Régression conso** : Random Forest Regressor

**Résultats** :
- Classe DPE prédite (A <-> G) 
- Consommation estimée
- Indication **MaPrimeRénov** (éligibilité simple) (E,F,G)

---

### ⚙️ API – Interface FastAPI

**Objectif** : Exposer les modèles de prédiction à travers une API REST performante et documentée, permettant l’accès aux fonctionnalités de calcul du DPE, de la consommation énergétique et de l’éligibilité à MaPrimeRénov’.  

L’API est construite avec **FastAPI**, intégrée directement à l’application Streamlit, et documentée automatiquement via Swagger (accessible à l’adresse `/docs`).

**🔗 Endpoints disponibles**

| Méthode | Endpoint | Description |
|----------|-----------|-------------|
| `GET` | `/status` | Vérifie la disponibilité et l’état du service |
| `GET` | `/last_update` | Renvoie la dernière date de mise à jour des données DPE |
| `GET` | `/predict_sample` | Permet une prédiction rapide via les paramètres d’URL |
| `POST` | `/predict_all` | Exécute une prédiction complète : étiquette DPE, consommation (kWh/m²/an) et éligibilité MaPrimeRénov’ |

**Autres fonctionnalités**
- Schéma des champs attendus (`POST /predict_all`)
- Exemple de corps JSON (POST)
- Outil de requête interactif permettant de tester directement les endpoints de l’API sans ligne de code.  

**⚙️ Fonctionnement global**

1. Les requêtes envoyées par Streamlit sont transmises à **FastAPI** (port `8000`)  
2. FastAPI charge les modèles `.pkl` hébergés localement ou sur **Hugging Face**  
3. Les prédictions sont renvoyées au format JSON à Streamlit (port `8501`)  
4. L’utilisateur visualise les résultats directement dans l’application  


---

### 👤 Profil
**Contenu** : Photos des membres de l'équipe + liens vers profils Linkedin.

---

## Fonctionnalités majeures

| Catégorie | Détails |
|---|---|
| Multi-pages Streamlit | Contexte, Exploration, Analyse, Cartographie, Prédiction, API |
| Visualisations | Plotly (interactif) & Folium (cartes) |
| Filtres dynamiques | Actualisation immédiate |
| Export | CSV (données filtrées), PNG (graphiques/carte) |
| API | `/predict_dpe` et `/predict_conso` |
| ML intégré | Random Forest (classif & régression) |
| Déploiement | Docker/Koyeb prêt |

---

## Cas d’usage typiques

| Objectif | Action | Résultat |
|---|---|---|
| Explorer les DPE | Onglet **Exploration** | Graphiques filtrables |
| Comprendre la conso | Onglet **Analyse** | Corrélations et tendances |
| Voir la répartition | Onglet **Cartographie** | Carte interactive |
| Simuler un logement | Onglet **Prédiction** | DPE & conso estimés |
| Tester l’API | Onglet **API** | Requêtes JSON live |

---

## Évolutions prévues
- Réentraînement des modèles depuis l’interface  
- Enrichissement des données (et des analyses) avec données OpenData

---

**Auteur** : Yassine CHENIOUR - Mohamed Habib BAH - Perrine IBOUROI  
**Date** : Octobre 2025  
**Version** : 1.0  
**Licence** : Usage académique – Master 2 SISE
