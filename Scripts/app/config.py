# scripts/app/config.py

from pathlib import Path

ROOT_DIR = Path(__file__).parents[2]
DATA_DIR = ROOT_DIR / "data"
MODEL_DIR = ROOT_DIR / "models"

# Remplace ceci :
# DEFAULT_DATA_FILE = "dataset_clean.csv"
# par :
DEFAULT_DATA_FILE = "donnees_dpe_71_clean.csv"

# Et indique le bon sous-dossier ("." = racine de data)
DEFAULT_DATA_SUBDIR = "."

# affichage dans la page 1_Contexte
MAX_ROWS_DISPLAY = 50