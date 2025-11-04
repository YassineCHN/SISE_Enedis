# 📘 Documentation Fonctionnelle – GreenTech Solutions

## Présentation du projet

**GreenTech Solutions** est une application web interactive combinant **Streamlit** (interface utilisateur) et **FastAPI** (API de prédiction), déployée sur **Koyeb**.  
Elle permet d’explorer les données du **Diagnostic de Performance Énergétique (DPE)** (ADEME), d’analyser la consommation énergétique des logements et de **prédire la classe DPE et la consommation estimée** d’un logement.

**URL de déploiement :** appstreamlit.koyeb.app
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
- Visualisations interactives (**Plotly**) : histogrammes, barres, scatter, boxplots
- Export : graphiques **PNG** et données filtrées **CSV**

**Utilisation** : Choisir les filtres (sidebar) → visuels mis à jour en temps réel.

---

### 📈 Analyse Statistique
**Objectif** : Étudier les relations entre caractéristiques des logements et performances énergétiques.  
**Fonctionnalités** :
- Corrélations : énergie ↔ consommation, période ↔ DPE, surface ↔ GES
- Graphiques Plotly (zoom, survol, export)

**Utilisation** : Identifier tendances globales et variables influentes.

---

### 🗺️ Cartographie
**Objectif** : Visualiser la répartition géographique des logements.  
**Fonctionnalités** :
- Carte **Folium** intégrée à Streamlit
- Conversion géographique **Lambert93 → WGS84**
- Filtres : classe DPE, période, type de bâtiment
- Navigation (zoom, clic) et **export image**

**Utilisation** : Explorer zones performantes vs énergivores.

---

### 🤖 Prédiction
**Objectif** : Simuler **classe DPE (A–G)** et **consommation (kWh/m²/an)**.  
**Formulaire** :
- Type (maison/appartement), surface, période/année de construction
- Énergie de chauffage
- Logement traversant (Oui/Non), qualité d’isolation

**Modèles** :
- **Classification DPE** : Random Forest Classifier  
- **Régression conso** : Random Forest Regressor

**Résultats** :
- Classe DPE prédite + badge “Passoire” (F–G)
- Consommation estimée
- Indication **MaPrimeRénov** (éligibilité simple)

---

### ⚙️ API
**Objectif** : Exposer les modèles via **FastAPI**.  
**Fonctionnalités** :
- Documentation interactive Swagger : `/docs`
- Endpoints : `/predict_dpe`, `/predict_conso`
- Exemple de payload :
```json
{
  "surface_habitable_logement": 85,
  "type_batiment": "maison",
  "type_energie_principale_chauffage": "electricite",
  "periode_construction": "1971 - 1980",
  "logement_traversant": "non"
}
```

---

### 👤 À propos
**Contenu** : Liens GitHub, auteurs/roles (chef de projet, dev, data scientist), liens doc technique & rapport d’étude.

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
- MAJ automatique des données via API ADEME  
- Réentraînement des modèles depuis l’interface  
- Mode “avant/après travaux” (comparaison scénarios)  
- Profils utilisateurs (sauvegarde scénarios)

---

**Auteur** : Yassine CHENIOUR - Mohamed Habib BAH - Perrine IBOUROI
**Date** : Octobre 2025  
**Version** : 1.0  
**Licence** : Usage académique – Master 2 SISE
