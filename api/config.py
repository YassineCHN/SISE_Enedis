import os

# Répertoires racine
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

MODELS_DIR = os.path.join(ROOT_DIR, "models")
DATA_DIR = os.path.join(ROOT_DIR, "data")

# Chemins vers les modèles
MODEL_DPE_PATH = os.path.join(MODELS_DIR, "model_DPE_Random_Forest.pkl")
MODEL_CONSO_PATH = os.path.join(MODELS_DIR, "model_CONSO_Random_Forest.pkl")

# Port API par défaut
API_PORT = int(os.getenv("API_PORT", 8000))
