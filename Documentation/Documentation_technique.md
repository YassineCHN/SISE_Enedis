# ⚙️ Documentation Technique – GreenTech Solutions

## 1. Architecture générale

L’application **GreenTech Solutions** repose sur une architecture moderne combinant **Streamlit** pour l’interface utilisateur et **FastAPI** pour le backend de prédiction.  
Elle est conteneurisée via **Docker** et déployée sur la plateforme **Koyeb**.

### Vue d’ensemble

```text
Utilisateur ↔ Streamlit (Frontend)
             ↕
          FastAPI (Backend)
             ↕
   Modèles ML (.pkl - Random Forest)
             ↕
   Données ADEME (CSV - DPE existants/neufs)
```

### Répartition des composants

| Répertoire | Rôle principal |
|-------------|----------------|
| `api/` | API FastAPI : endpoints de prédiction et chargement des modèles |
| `Scripts/app/` | Application Streamlit (frontend) avec les pages et les utilitaires |
| `models/` | Modèles ML sauvegardés (`.pkl`) |
| `data/` | Jeux de données ADEME nettoyés (CSV) |
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

## 6. Schéma d’architecture

L’illustration ci-dessous représente l’architecture globale du projet.

![Architecture GreenTech Solutions](architecture_greentech.png)

### Description du flux :
1. L’utilisateur interagit via **Streamlit**
2. Les requêtes de prédiction sont envoyées à **FastAPI**
3. FastAPI charge les modèles `.pkl` pour l’inférence
4. Les résultats sont renvoyés à Streamlit pour affichage
5. L’application est conteneurisée et déployée sur **Koyeb**

---

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
