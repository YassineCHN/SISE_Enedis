import os
import joblib

def load_model(path: str):
    """Charge un modèle depuis le chemin spécifié."""
    if not os.path.exists(path):
        print(f"[⚠️] Modèle introuvable : {path}")
        return None
    try:
        model = joblib.load(path)
        print(f"✅ Modèle chargé : {os.path.basename(path)}")
        return model
    except Exception as e:
        print(f"[❌] Erreur chargement modèle {path}: {e}")
        return None
