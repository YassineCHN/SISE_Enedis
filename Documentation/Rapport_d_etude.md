# 🧠 Rapport d’étude – Projet GreenTech Solutions  
### Diagnostic de Performance Énergétique (DPE) & Prédiction de Consommation  
_M2 SISE – Octobre 2025_

---

## 1. Introduction et contexte

Avec la hausse du coût de l’énergie et les objectifs de neutralité carbone, le **Diagnostic de Performance Énergétique (DPE)** est devenu un indicateur clé de la transition énergétique des logements.  
Le projet GreenTech Solutions, mené pour **Enedis**, vise à :

- Explorer les données publiques du DPE disponibles sur la plateforme **ADEME OpenData**.  
- Identifier les facteurs influençant la performance énergétique des logements.  
- Construire des modèles de **classification** et **régression** permettant de prédire :  
  - la **classe DPE (A à G)**,  
  - la **consommation énergétique (kWh/m²/an)**.

L’application finale permet à un utilisateur de :
1. Explorer les données de DPE d’un territoire (ici, **Savoie – 73**)  
2. Visualiser les indicateurs et cartes interactives  
3. Simuler ou prédire la performance énergétique d’un logement

---

## 2. Collecte des données

### 2.1 Sources
Les données ont été extraites des **API officielles de l’ADEME** :
- [`dpe-v2-logements-existants`](https://data.ademe.fr/datasets/dpe-v2-logements-existants)
- [`dpe-v2-logements-neufs`](https://data.ademe.fr/datasets/dpe-v2-logements-neufs)

### 2.2 Extraction
- Département étudié : **73 – Savoie**
- Période : 2021 → 2025  
- Volume collecté :
  - 110 526 DPE existants  
  - 10 816 DPE neufs
- Requêtes paginées et itératives pour chaque année
- Gestion des erreurs et reprise automatique en cas de coupure

> 📁 Fichiers produits :  
> `../data/donnees_dpe_existants_73.csv`  
> `../data/donnees_dpe_neufs_73.csv`

---

## 3. Préparation des données

### 3.1 Fusion et enrichissement
Les deux jeux ont été fusionnés après ajout de la variable `Logement` (Ancien / Neuf) et création de la colonne `annee_construction`.

> 📊 **Taille initiale** : 117 708 lignes × 211 colonnes

### 3.2 Création de variables
- **Année de réception du DPE** → `annee_reception_DPE`  
- **Période de construction** → 7 classes de périodes (`Avant 1960` → `Après 2010`)  
- **Filtrage des types de bâtiments** → uniquement *maisons* et *appartements*

> Répartition après filtrage :
> - Appartement : 96 964  
> - Maison : 20 744  

### 3.3 Conversion géographique
Les coordonnées Lambert93 ont été converties en WGS84 pour la cartographie.

| X (Lambert93) | Y (Lambert93) | Longitude | Latitude |
|----------------|----------------|------------|-----------|
| 927396.82 | 6518105.11 | 5.924250 | 45.724631 |
| 946042.17 | 6501898.56 | 6.155453 | 45.572340 |
| 912675.52 | 6492089.43 | 5.723560 | 45.495255 |

### 3.4 Nettoyage
- Suppression de 2 colonnes totalement vides  
- Suppression de 4 colonnes techniques inutiles (`_geopoint`, `_id`, `_rand`, `_i`)  
- Taux moyen de valeurs manquantes : **33,61 % → 8,99 %**  
- Suppression de **62 colonnes** avec plus de 50 % de valeurs manquantes  

> 📊 **Dataset final :** 117 708 lignes × 143 colonnes  
> 📁 Export : `../data/donnees_dpe_73_clean.csv`

---

## 4. Méthodologie et modélisation

### 4.1 Variables explicatives principales
Les modèles utilisent un sous-ensemble homogène de 9 variables :
- annee_construction,
- surface_habitable_logement,
- type_batiment,
- type_energie_principale_chauffage,
- classe_inertie_batiment,
- qualite_isolation_murs,
- qualite_isolation_menuiseries,
- classe_altitude,
- logement_traversant


### 4.2 Prétraitement
- **Encodage catégoriel** : `OneHotEncoder`
- **Mise à l’échelle** : `StandardScaler`
- **Pipeline Scikit-learn** : `ColumnTransformer` + modèle ML

### 4.3 Modélisation

#### 🔹 Modèle de régression – Consommation énergétique
- Objectif : prédire la **consommation finale (kWh/m²/an)**  
- Modèles testés :
  - Linear Regression  
  - Gradient Boosting Regressor  
  - Random Forest Regressor ✅

**Performances finales :**
| Métrique | Valeur |
|-----------|--------|
| R² | **0.72** |
| RMSE | 78.2 |
| MAE | 47.1 |

**Modèle retenu : Random Forest Regressor**  
> Sauvegarde : `/models/model_CONSO_Random_Forest.pkl`

---

#### 🔹 Modèle de classification – Classe DPE (A→G)
- Objectif : prédire la classe énergétique d’un logement  
- Modèles testés :
  - Logistic Regression  
  - Gradient Boosting Classifier  
  - Random Forest Classifier ✅

**Performances finales :**
| Métrique | Valeur |
|-----------|--------|
| Accuracy | **0.64** |
| F1-macro | 0.61 |

> Modèle retenu : Random Forest Classifier  
> Sauvegarde : `/models/model_DPE_Random_Forest.pkl`

---

#### 🔹 Modèle binaire – Éligibilité MaPrimeRénov
- Objectif : classer les logements éligibles au dispositif MPR  
- Cible : E–F–G = 1 (éligible) / A–D = 0  
- Modèle retenu : Random Forest Classifier ✅

| Métrique | Valeur |
|-----------|--------|
| AUC | **0.95** |
| F1-macro | 0.87 |

> Sauvegarde : `/models/model_MPR_Random_Forest.pkl`

---

## 5. Interprétation des résultats

### 5.1 Analyse des performances
- Les modèles de **forêts aléatoires** offrent un excellent compromis entre robustesse et interprétabilité.  
- Les scores obtenus sont satisfaisants au vu de la diversité et de l’hétérogénéité des données ADEME.

| Modèle | Type | Métrique principale | Valeur |
|---------|------|----------------------|---------|
| Random Forest | Régression | R² | 0.72 |
| Random Forest | Classification DPE | Accuracy | 0.64 |
| Random Forest | Classification MPR | AUC | 0.95 |

---

### 5.2 Variables les plus influentes
Les analyses de `feature_importances_` indiquent que :
- L’**année de construction**,  
- La **qualité d’isolation des murs et menuiseries**,  
- Le **type d’énergie de chauffage**,  
sont les déterminants principaux de la performance énergétique.

---

## 6. Tests et validation

| Scénario | Description | Prédiction DPE | MaPrimeRénov | Conso (kWh/m²/an) |
|-----------|--------------|----------------|---------------|--------------------|
| Maison récente (élec) | Maison récente | B | ❌ Non | 119.7 |
| Appartement ancien (fioul) | Appartement ancien | G | ✅ Oui | 428.1 |
| Maison ancienne (bois) | Maison ancienne | D | ❌ Non | 254.4 |

Les prédictions sont cohérentes avec la logique énergétique observée.

---

## 7. KPI et synthèse

| Indicateur | Valeur | Interprétation |
|-------------|---------|----------------|
| R² régression | 0.72 | 72 % de la variabilité de la consommation expliquée |
| F1-macro DPE | 0.61 | Bon équilibre entre classes du DPE |
| AUC MPR | 0.95 | Excellent pouvoir discriminant |
| Taux de valeurs manquantes | 8.99 % | Dataset propre et exploitable |

---

## 8. Conclusions et perspectives

Les modèles mis en place permettent une **prédiction fiable et automatisée** des performances énergétiques à partir des caractéristiques principales du logement.

**Axes d’amélioration possibles :**
- Intégrer des données météorologiques et socio-économiques (OpenData)
- Raffiner le feature engineering (zones climatiques, altitude réelle)
- Optimiser les hyperparamètres via GridSearchCV
- Mettre en place un réentraînement automatique via FastAPI (module `retrain`)

---

🧾 **Résumé global :**
> Le projet GreenTech Solutions démontre la faisabilité d’un système intégré **Streamlit + FastAPI** pour la visualisation, l’analyse et la prédiction du DPE.  
> Les modèles Random Forest offrent des performances solides et une intégration fluide dans l’application déployée sur Koyeb.

---
