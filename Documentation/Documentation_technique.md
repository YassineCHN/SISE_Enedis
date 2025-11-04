# ⚙️ Documentation Technique – GreenTech Solutions

## 1. Architecture générale

L’application **GreenTech Solutions** repose sur une architecture moderne combinant **Streamlit** pour l’interface utilisateur et **FastAPI** pour le backend de prédiction.  
Elle est conteneurisée via **Docker** et déployée sur la plateforme **Koyeb**.

### Vue d’ensemble

<img width="1920" height="1080" alt="M2SIA- Diapo soutenance  (1)" src="https://github.com/user-attachments/assets/5542a144-19c7-4909-b1fb-6d6650529701" />


### Répartition des composants

| Répertoire | Rôle principal |
|-------------|----------------|
| `api/` | API FastAPI : endpoints de prédiction et chargement des modèles |
| `Scripts/app/` | Application Streamlit (frontend) avec les pages et les utilitaires |
| `models/` | Modèles ML sauvegardés (`.pkl`) |
| `data/` | Jeux de données ADEME nettoyés (CSV) |
| `Hugging Face` | Stockage des datasets et modèles pour les rendre accessibles par l'app koyeb |
| `volume` | Stockage persistant des datasets et modèles sur koyeb |
| `Notebooks/` | Scripts de modélisation (collecte, préparation, entraînement) |
| `Dockerfile` | Image combinée Streamlit + FastAPI |
| `koyeb.yaml` | Configuration de déploiement sur Koyeb |

---

## 2. Composants logiciels

### 2.1 Backend – FastAPI

**Fichier principal :** `api/main.py`  
**Objectif :** fournir des endpoints REST pour les prédictions de DPE et de consommation.

**Endpoints principaux :**
| Endpoint | Méthode | Description |
|-----------|----------|-------------|
| `/predict_dpe` | POST | Prédiction de la classe énergétique (A–G) |
| `/predict_conso` | POST | Prédiction de la consommation (kWh/m²/an) |

**Modules :**
- `schemas.py` : Définition des schémas Pydantic pour valider les requêtes
- `models_loader.py` : Chargement des modèles `.pkl` depuis le dossier `models/`
- `utils.py` : Fonctions utilitaires
- `config.py` : Paramètres d’initialisation

**Librairies clés :** `fastapi`, `uvicorn`, `pydantic`, `joblib`, `scikit-learn`

---

### 2.2 Frontend – Streamlit

**Point d’entrée :** `Scripts/app/main.py`  
**Framework :** Streamlit multi-pages

**Structure :**
- `pages/` : contient les pages Contexte, Exploration, Analyse, Cartographie, Prédiction, API
- `utils/` : fonctions partagées (préprocessing, visualisation, chargement des données)
- `assets/` : images et icônes
- `config.py` : paramètres généraux (thème, titre, favicon, etc.)

**Librairies principales :** `streamlit`, `plotly`, `streamlit_folium`, `pandas`, `folium`, `pyproj`

---

## 3. Environnements et dépendances

**Python :** 3.12  
**Environnement virtuel :** `venv_enedis`

### Fichier `requirements.txt`
Inclut notamment :  
`streamlit`, `fastapi`, `uvicorn`, `scikit-learn`, `pandas`, `numpy`, `plotly`, `folium`, `requests`, `joblib`, `pydantic`, `pyproj`.

---

## 4. Exécution du projet

### En local
```bash
# 1. Activer l'environnement virtuel
venv_enedis\Scripts\activate

# 2. Lancer l'API
uvicorn api.main:app --reload

# 3. Lancer Streamlit
streamlit run Scripts/app/main.py
```

**URL locales :**
- Streamlit : http://localhost:8501  
- API FastAPI : http://localhost:8000/docs

---
### 🚀 Exécuter le projet avec Docker

Ce projet peut être lancé de **deux manières** :  
1) **Construire l’image localement** à partir du Dockerfile  
2) **Télécharger l’image publique** depuis Docker Hub

---

#### 🧩 Prérequis
- Docker installé (Windows/macOS/Linux)
- Ports **8000** (API FastAPI) et **8501** (Streamlit) libres

---

#### ✅ Option A — Construire l’image localement

```bash
# Se placer à la racine du projet (là où se trouve le Dockerfile)
docker build -t dpe-app .

# Lancer le conteneur
docker run -p 8000:8000 -p 8501:8501 dpe-app
```

**Accès locaux :**
- Streamlit : http://localhost:8501  
- API FastAPI : http://localhost:8000/docs

---

#### ✅ Option B — Utiliser l’image publique (Docker Hub)

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-dpe--app-blue?logo=docker)](https://hub.docker.com/r/yassinechn/dpe-app)

Téléchargez et lancez l’image **sans dépendances locales** :

```bash
# Télécharger l’image publique
docker pull yassinechn/dpe-app:latest

# Lancer le conteneur
docker run -p 8000:8000 -p 8501:8501 yassinechn/dpe-app:latest
```

**Accès locaux :**
- Streamlit : http://localhost:8501  
- API FastAPI : http://localhost:8000/docs

---

#### 📦 Détails techniques de l’image

| Élément | Valeur |
|---|---|
| **Image locale** | `dpe-app:latest` |
| **Image publique** | `yassinechn/dpe-app:latest` |
| **Base** | `python:3.12-slim` |
| **Taille indicative** | ≈ 2.9 GB |
| **Ports exposés** | `8000` (FastAPI), `8501` (Streamlit) |
| **Volumes** | `/app/data`, `/app/models` |
| **Compatibilité** | Windows / macOS / Linux |

---

#### 🛠️ Dépannage (FAQ rapide)

- **Port déjà utilisé (Bind for 0.0.0.0:8000 failed)**  
  → Arrêter le service qui occupe le port ou changer le mapping, ex. :  
  ```bash
  docker run -p 8080:8000 -p 8501:8501 dpe-app
  ```
  Accès API : http://localhost:8080/docs

- **Rebuild nécessaire après modification du code**  
  → Reconstruire l’image :  
  ```bash
  docker build -t dpe-app .
  ```
💡 *Cette image permet d’exécuter le projet complet
---

---

### Déploiement sur Koyeb

**Fichier :** `koyeb.yaml`

```yaml
name: dpe-streamlit-app
services:
  - name: dpe-streamlit
    type: web
    ports:
      - 8501
    routes:
      - path: /
    build_from_source: true
    dockerfile_path: ./Dockerfile
    volumes:
      - name: data-volume
        mount_path: /app/data
      - name: models-volume
        mount_path: /app/models
    env:
      - key: STREAMLIT_SERVER_PORT
        value: "8501"
      - key: PYTHONUNBUFFERED
        value: "1"
```

**Commandes exécutées automatiquement :**
- Démarrage de FastAPI (`uvicorn api.main:app`)  
- Lancement de Streamlit (`streamlit run Scripts/app/main.py`)

---

## 5. Maintenance et évolution

| Tâche | Localisation | Description |
|--------|---------------|--------------|
| 🔁 Réentraînement | `Notebooks/classification_new.ipynb` & `regression_new.ipynb` | Réentraîner et sauvegarder les nouveaux modèles `.pkl` |
| 🧹 Rafraîchissement des données | `Notebooks/collect_data_api.ipynb` | Mise à jour depuis l’API ADEME |
| 🧰 Mise à jour dépendances | `requirements.txt` | `pip install -r requirements.txt` |
| 🐳 Reconstruction Docker | `Dockerfile` | `docker build -t dpe-app .` |
| ☁️ Mise à jour sur Koyeb | `koyeb.yaml` | Relancer le déploiement avec `git push` |

---

## 6. Schéma d’architecture – GreenTech Solutions

L’architecture globale du projet **GreenTech Solutions** combine un pipeline **ETL complet**, un module de **modélisation Machine Learning**, et une **application web conteneurisée** (Streamlit + FastAPI) déployée sur **Koyeb**.  
Elle intègre également **Hugging Face** pour le stockage distant et la synchronisation automatique des modèles et jeux de données.
L’ensemble est conteneurisé via **Docker** et déployé sur **Koyeb**.

---

### 🧩 6.1 – Pipeline ETL (Collecte, Transformation, Modélisation)

Ce premier schéma illustre le processus complet de préparation des données et d’entraînement des modèles :

1. **Collecte (Extract)**  
   - En début de script on attribue (manuellement) une valeur d'un nombre entier à la variable DEPT_CODE (qui dans le schéma est appelé "dept")  afin de choisir le département que l'on veut récupérer
   - Récupération des DPE *existants* et *neufs* via les **API publiques ADEME** (`dpe03existant`, `dpe02neuf`) à l’aide de `requests` et `pandas` sur le DEPT_CODE renseigné. 
   - Export en CSV (`donnees_dpe_[dept]_existants.csv`, `donnees_dpe_[dept]_neufs.csv`).

2. **Transformation (Transform)**  
   - Nettoyage, fusion, ajout de colonnes, conversion des coordonnées (Lambert93 → WGS84).
   - Production du fichier propre `donnees_dpe_[dept]_clean.csv`.

3. **Modélisation et entraînement (Load/Restitution)**  
   - Entraînement des modèles de **régression** (consommation énergétique) et de **classification** (étiquette DPE, éligibilité MaPrimeRénov’)  
   - Sauvegarde des modèles au format `.pkl` :  
     - `model_CONSO_Random_Forest.pkl`  
     - `model_DPE_Random_Forest.pkl`  
     - `model_MPR_Random_Forest.pkl`

4. **Publication sur Hugging Face (Synchronisation)**  
   - Les fichiers modèles et datasets nettoyés sont **envoyés sur le dépôt Hugging Face** pour être accessibles publiquement lors du déploiement sur Koyeb.  
   - Hugging Face agit comme **stockage distant partagé** entre l’environnement local et le cloud.

📘 **Notebooks concernés :**  
`collect_data_api.ipynb`, `prepare_data.ipynb`, `regression_new.ipynb`, `classification_new.ipynb`

🧠 **Technos principales :** `pandas`, `numpy`, `pyproj`, `scikit-learn`, `joblib`, `huggingface_hub`

📊 **Schéma ETL :**
<img width="1920" height="1080" alt="M2SIA- Diapo soutenance  (3)" src="https://github.com/user-attachments/assets/6a3a333e-0308-4f06-9f65-86670c8cf133" />

---

### 💻 6.2 – Architecture applicative (Streamlit + FastAPI)

L’application combine une interface utilisateur **Streamlit** et un backend **FastAPI**.  
Les deux sont lancés simultanément dans le même conteneur Docker.

- **Streamlit** pour le front-end interactif (multi-pages)
- **FastAPI** pour le back-end de prédiction

**Fonctionnement général :**
1. L’utilisateur interagit avec Streamlit à travers plusieurs pages :  
   `/Contexte`, `/Exploration`, `/Analyse`, `/Cartographie`, `/Prédiction`, `/API`, `/Profil`
2. Lorsqu’une prédiction est demandée, Streamlit envoie une requête HTTP à FastAPI.
3. FastAPI charge les modèles `.pkl` et renvoie les résultats à Streamlit pour affichage.

**Chargement des modèles :**
- Au démarrage du conteneur, un script (`init_assets.py`) télécharge automatiquement les modèles et jeux de données depuis **Hugging Face** si absents du volume local.  
- Les fichiers sont ensuite placés dans `/app/models` et `/app/data`.

**Endpoints FastAPI principaux :**
| Méthode | Endpoint | Description |
|----------|-----------|-------------|
| `GET` | `/status` | Vérifie la disponibilité du service |
| `GET` | `/last_update` | Indique la date de dernière mise à jour des modèles |
| `GET` | `/predict_sample` | Fournit un exemple de prédiction |
| `POST` | `/predict_all` | Réalise une prédiction complète (DPE, consommation, MaPrimeRénov’) |

🌐 **Ports utilisés :**
- `8501` → Streamlit  
- `8000` → FastAPI  

📘 **Dossiers concernés :**
- `/Scripts/app/` → Interface Streamlit (frontend)  
- `/api/` → API FastAPI (backend)  
- `/models/` → Modèles ML `.pkl`  
- `/data/` → Données ADEME nettoyées

📊 **Schéma application :**
<img width="1920" height="1080" alt="M2SIA- Diapo soutenance " src="https://github.com/user-attachments/assets/4a6f9d5c-b203-4b48-95dc-46a41b10803b" />

---

### ☁️ 6.3 – Déploiement global (Docker + Koyeb + Hugging Face)

L’ensemble de la solution est conteneurisé et déployé sur la plateforme **Koyeb** à l’aide du `Dockerfile` et du fichier `koyeb.yaml`.

**Étapes de fonctionnement :**

1. **Construction Docker** : le Dockerfile crée une image contenant Streamlit, FastAPI et les dépendances ML.  
2. **Synchronisation avec Hugging Face** : lors du démarrage, les modèles et données sont automatiquement téléchargés dans les volumes `/app/data` et `/app/models`.  
3. **Déploiement Koyeb** : la plateforme lance le conteneur, expose les ports 8501 (Streamlit) et 8000 (FastAPI) et monte les volumes persistants.  
4. **Accès utilisateur** : via l’URL publique Koyeb.

📦 **Technos clés :** `Docker`, `Koyeb`, `Hugging Face`, `FastAPI`, `Streamlit`

📊 **Schéma global :**
<img width="1920" height="1080" alt="M2SIA- Diapo soutenance  (1)" src="https://github.com/user-attachments/assets/5542a144-19c7-4909-b1fb-6d6650529701" />

---

### 🔁 Résumé des interactions

| Étape | Entrées | Sorties | Technologies |
|--------|----------|----------|---------------|
| Collecte | API ADEME | CSV bruts | `requests`, `pandas` |
| Préparation | CSV bruts | `donnees_dpe_clean.csv` | `pandas`, `pyproj` |
| Modélisation | CSV clean | `.pkl` (modèles ML) | `scikit-learn`, `joblib` |
| Publication | `.pkl` + CSV clean | Hugging Face Hub | `huggingface_hub` |
| Application | `.pkl` + données | Interface Streamlit + API | `Streamlit`, `FastAPI` |
| Déploiement | Dockerfile + volumes | Service web Koyeb | `Docker`, `Koyeb` |

---

💡 *Hugging Face sert ici de pont entre l’environnement local et le cloud : les modèles et datasets sont centralisés et synchronisés automatiquement lors du déploiement.*


## 7. Bonnes pratiques
- Conserver la cohérence des versions de `scikit-learn` entre entraînement et production.  
- Vérifier que les volumes `/app/data` et `/app/models` sont bien montés avant chaque déploiement.  
- Utiliser `joblib` pour sérialiser les modèles et preprocessors.  
- Sauvegarder les notebooks avant tout réentraînement.  

---

## 8. Références
- [API ADEME – Données DPE](https://data.ademe.fr/)  
- [Documentation Streamlit](https://docs.streamlit.io/)  
- [Documentation FastAPI](https://fastapi.tiangolo.com/)  
- [Documentation Koyeb](https://www.koyeb.com/docs)  
