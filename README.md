# 🌿 GreenTech Solutions – France Énergie
> [!NOTE]
> Projet académique réalisé dans le cadre du Master 2 SISE (2025).

---

## Présentation
### 🔗 Live : [GreenTech Solutions sur Koyeb](https://appstreamlit.koyeb.app/) 

**GreenTech Solutions** est une application web interactive combinant **Streamlit** (interface utilisateur) et **FastAPI** (backend de prédiction).  
Elle permet d'explorer et d'analyser les données du **Diagnostic de Performance Énergétique (DPE)** et de **prédire la classe énergétique (A–G)** ainsi que la **consommation énergétique (kWh/m²/an)** d’un logement.

L’application vise à :
- Mieux comprendre la performance énergétique des logements français,
- Accompagner la transition énergétique et la sobriété,
- Sensibiliser aux aides comme **MaPrimeRénov’** (aide versée par l’Agence nationale de l’habitat (Anah) pour les rénovations de logements trop consommateur : E,F,G).

---

## 🖥️ Aperçu de l’application

### Page d’accueil – Contexte & Page Prédiction – Simulation énergétique
<p align="center">
  <img src="https://github.com/user-attachments/assets/288971bc-38c0-4e3c-9571-30e35b618f90" alt="Capture 1" width="48%" />
  <img src="https://github.com/user-attachments/assets/00c7d24f-3fd6-4d2d-a0db-3666c40619b8" alt="Capture 2" width="48%" />
</p>


---

## ⚙️ Technologies utilisées

| Composant | Technologie |
|------------|--------------|
| Frontend | **Streamlit** |
| Backend | **FastAPI** |
| Modélisation | **Scikit-learn**, **Pandas**, **Joblib** |
| Visualisation | **Plotly**, **Folium**, **Streamlit Folium** |
| Données géographiques | **PyProj** (conversion Lambert93 → WGS84) |
| Déploiement | **Docker**, **Koyeb** |

---

## 📊 Sources de données

Les données proviennent des APIs officielles :  
- [ADEME – DPE existants](https://data.ademe.fr/datasets/dpe03existant)  
- [ADEME – DPE neufs](https://data.ademe.fr/datasets/dpe02neuf)  

---

## 🧰 Installation et exécution

### 💻 En local
1. Cloner le projet :
   ```bash
   git clone https://github.com/.../SISE_ENEDIS.git
   cd SISE_ENEDIS
   ```
2. Créer et activer un environnement virtuel :
   ```bash
   python -m venv venv_enedis
   venv_enedis\Scripts\activate
   ```
3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Lancer l’API et l’application Streamlit (se placer dans le projet à la racine ENEDIS pour executer) :
   ```bash
   uvicorn api.main:app --reload
   streamlit run Scripts/app/main.py
   ```
5. Accès :
   - Application : [http://localhost:8501](http://localhost:8501)
   - API Swagger : [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 🐳 Avec Docker
```bash
# Construire l’image Docker
docker build -t dpe-app .

# Lancer le conteneur
docker run -p 8000:8000 -p 8501:8501 dpe-app
```
- L’API est disponible sur le port `8000`
- L’application Streamlit sur le port `8501`

---
ℹ️ **Note :**  
La description complète de l’image Docker publique (`yassinechn/dpe-app`) et les instructions de déploiement sont disponibles dans la  
📄 **[Documentation technique – Section “Image Docker publique”](Documentation/Documentation_technique.md)**.

## 📋 Cahier des charges

L’avancement du projet respecte la quasi-totalité des exigences du cahier des charges initial.  
Les fonctionnalités majeures (exploration, cartographie, prédiction, export, API, Docker) sont **fonctionnelles**.

### État d’avancement
<img width="1334" height="738" alt="image" src="https://github.com/user-attachments/assets/5938b80a-f26a-46dc-981a-e4b3f9be8cf6" />

<img width="1347" height="754" alt="image" src="https://github.com/user-attachments/assets/5281aa8a-c8c1-496e-ae99-2b076e75ccf0" />


### Suivi de projet – Taiga (remplaçant Azure DevOps)
<img width="1912" height="915" alt="image" src="https://github.com/user-attachments/assets/7a859124-f187-4471-bb29-719721d55a5f" />


> Bien que le suivi n’ait pas été exhaustif, le Kanban montre les principales étapes validées :  
> création du repo, rédaction du rapport, documentation, dockerisation et déploiement.

---

## 📈 Modèles de Machine Learning intégrés

| Modèle | Type | Objectif | Score principal |
|---------|------|-----------|-----------------|
| Random Forest Regressor | Régression | Prédiction consommation (kWh/m²/an) | R² = 0.72 |
| Random Forest Classifier | Classification | Prédiction étiquette DPE (A–G) | Accuracy = 0.64 |
| Random Forest Classifier | Binaire | Éligibilité MaPrimeRénov’ | AUC = 0.95 |

Les modèles sont stockés dans le dossier `/models` et chargés automatiquement par **FastAPI**.

---

## 🧱 Structure du projet

```
SISE_ENEDIS/
├── api/                  → Backend FastAPI
├── Scripts/app/           → Application Streamlit
│   ├── pages/             → Contexte, Exploration, Analyse, Cartographie, Prédiction, API
│   ├── utils/             → Data loading, visualisation, preprocessing
│   ├── assets/            → Images et icônes
├── data/                  → Jeux ADEME nettoyés
├── models/                → Modèles ML (.pkl)
├── Notebooks/             → Collecte, préparation, modélisation
├── Dockerfile             → Image combinée FastAPI + Streamlit
├── koyeb.yaml             → Configuration de déploiement cloud
└── README.md
```

---

## 👥 Crédits

**Auteur** : Yassine CHENIOUR - Mohamed Habib BAH - Perrine IBOUROI
**Date** : Octobre 2025  
**Version** : 1.0  
**Licence** : Usage académique – Master 2 SISE
