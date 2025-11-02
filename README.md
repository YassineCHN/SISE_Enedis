# SISE_Enedis

## À propos
Cette aplication a pour but de prédire une étiquette de diagnostic de performance énergétique ainsi que la consommation énergétique totale d'un logement.
Elle se base sur les données issues de l'ADEME https://data.ademe.fr/datasets et filtrées sur le département du Rhône.

## Table des matières  
- [Installation](#installation)  
- [Structure du projet](#structure-du-projet)  
- [Utilisation](#utilisation)  
- [Données](#données)  
- [Contribuer](#contribuer)
- [Auteurs](#auteurs)



## Installation
Ces informations sont disponibles dans la [documentation technique](https://github.com/YassineCHN/SISE_Enedis/tree/main/Documentations).

#### 1. Cloner le dépôt :
git clone https://github.com/YassineCHN/SISE_Enedis.git
cd SISE_Enedis  
#### 2. Créer un environnement virtuel: 
python -m venv venv
source venv/bin/activate 
#### 3. Installer les dépendances:
pip install -r requirements.txt

## Structure du projet
Voici une présentation de la structure du projet:

SISE_Enedis/

├── data/               *# Jeux de données*  
├── Notebooks/          *# Notebooks Jupyter d’analyse exploratoire*  
├── Scripts/            *# Scripts Python pour traitement, modélisation, interface*  
├── Modèle/             *# Fichiers relatifs au modèle (par ex. model.py)*  
├── Documentations/     *# Documentation, manuel utilisateur, guide Git*  
├── api.py              *# Module API (si l’application utilise une API)*  
├── requirements.txt    *# Liste des dépendances Python*  
└── README.md           *# Ce fichier*


Le lancement de l'application se fait via le fichier app.py contenu dans le dossier Scripts

## Utilisation
Activez votre environnement virtuel dans lequel vous avez installé les dépendances contenues dans requirements.txt. 
Ensuite, dans le terminal, lancez l'application via la commande `streamlit run app.py` (si vous vous trouvez bien à l'emplacement du fichier app.py, sinon indiquez le chemin absolu)

## Données 
Les données utilisées proviennent de l'ADEME. Une requête via l'API de l'Ademe a permis de stocker les données sous format .csv. Les données peuvent être rafraîchies via l'application directement.

## Contribuer 
Les contributions sont les bienvenues. 
Pour cela : 

1- Forkez ce dépôt.

2- Créez une branche : git checkout -b feature/ma‑nouvelle‑fonctionnalité

3- Faites vos modifications et commitez : git commit -m "Ajout de …"

4- Pushez : git push origin feature/ma‑nouvelle‑fonctionnalité

Ouvrez une Pull Request sur ce dépôt.
Veuillez aussi ajouter des tests/unités ou un notebook de démonstration si applicable.

## Auteurs
- [YassineCHN](https://github.com/YassineCHN)
- [Bahmohamedhabib](https://github.com/Bahmohamedhabib)
- [perrineib](https://github.com/perrineib)