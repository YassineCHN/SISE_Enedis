# ============================================================
# 🔌 API Modèles Énergie — main.py (SISE_Enedis)
# ============================================================

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib, os

from api.config import MODEL_DPE_PATH, MODEL_CONSO_PATH
from models_loader import load_model
from schemas import InputFeatures
from utils import normalize_input
import requests

# ------------------------------------------------------------
# ⚙️ Initialisation FastAPI
# ------------------------------------------------------------
app = FastAPI(
    title="API Modèles Énergie",
    description=(
        "API pour prédire l’étiquette DPE et la consommation (kWh/m²/an) "
        "à partir des caractéristiques d’un logement."
    ),
    version="1.2.0",
)

# Autoriser l'accès depuis Streamlit/local (adapter si besoin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restreindre si nécessaire
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# 📦 Chargement des modèles et préprocesseur
# ------------------------------------------------------------
model_dpe = load_model(MODEL_DPE_PATH)
model_conso = load_model(MODEL_CONSO_PATH)

PREPROC_PATH = os.path.join(os.path.dirname(MODEL_CONSO_PATH), "preprocessor_conso.pkl")
preproc_conso = joblib.load(PREPROC_PATH) if os.path.exists(PREPROC_PATH) else None

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "donnees_dpe_73_clean.csv")
DATA_PATH = os.path.abspath(DATA_PATH)

# ------------------------------------------------------------
# 🧭 Routes générales (GET)
# ------------------------------------------------------------
@app.get("/")
def root():
    """Message d'accueil de l'API"""
    return {"message": "Bienvenue sur l'API Modèles Énergie 🔋"}

@app.get("/status")
def status():
    """Vérifie le statut et le chargement des modèles"""
    return {
        "status": "ok",
        "models": {
            "DPE": model_dpe is not None,
            "Conso": model_conso is not None,
            "Preprocessor_CONSO": preproc_conso is not None
        }
    }

@app.get("/last_update")
def get_last_update():
    """
    Retourne la date la plus récente de réception DPE
    (utile pour vérifier les nouvelles données à importer).
    """
    try:
        df = pd.read_csv(DATA_PATH)
        if "date_reception_dpe" not in df.columns:
            raise ValueError("Colonne 'date_reception_dpe' absente du dataset")
        last_date = pd.to_datetime(df["date_reception_dpe"], errors="coerce").max()
        return {"last_update": str(last_date.date())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lecture dataset : {e}")

# ------------------------------------------------------------
# 🔮 Prédictions (POST & GET)
# ------------------------------------------------------------
@app.post("/predict_all")
def predict_all(data: InputFeatures):
    """
    Retourne l’étiquette DPE prédite et la consommation estimée (kWh/m²/an).
    """
    try:
        df = pd.DataFrame([data.dict()])
        df = normalize_input(df)

        # logement_traversant arrive en "oui"/"non" -> convertir en 0/1 pour les modèles si nécessaire
        if "logement_traversant" in df.columns:
            df["logement_traversant"] = df["logement_traversant"].apply(
                lambda x: 1 if str(x).strip().lower() in ["oui", "true", "1"] else 0
            )

        # --- DPE ---
        dpe_pred = model_dpe.predict(df)[0] if model_dpe is not None else None

        # --- Conso ---
        conso_pred = None
        if model_conso is not None:
            if preproc_conso is not None:
                X_trans = preproc_conso.transform(df)
                conso_pred = model_conso.predict(X_trans)[0]
            else:
                conso_pred = model_conso.predict(df)[0]

        return {
            "DPE": str(dpe_pred),
            "Conso_kWh_m2": round(float(conso_pred), 2) if conso_pred is not None else None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {e}")

@app.get("/predict_sample")
def predict_sample(
    annee_construction: int = Query(1990),
    surface_habitable_logement: float = Query(80.0),
    type_batiment: str = Query("maison"),
    type_energie_principale_chauffage: str = Query("Électricité")
):
    """
    Prédiction simplifiée (GET) via paramètres d’URL (pour tests rapides).
    Exemple :
    /predict_sample?annee_construction=1980&surface_habitable_logement=100&type_batiment=maison&type_energie_principale_chauffage=Gaz%20naturel
    """
    try:
        sample = {
            "annee_construction": annee_construction,
            "surface_habitable_logement": surface_habitable_logement,
            "type_batiment": type_batiment,
            "classe_inertie_batiment": "Moyenne",
            "qualite_isolation_murs": "moyenne",
            "qualite_isolation_menuiseries": "moyenne",
            "classe_altitude": "400-800m",
            "logement_traversant": "oui",
            "type_energie_principale_chauffage": type_energie_principale_chauffage,
            "periode_construction": "1989-2000",
            "energie_chauffage": "Électricité",
            "zone_climatique": "H1"
        }

        df = pd.DataFrame([sample])
        df = normalize_input(df)
        df["logement_traversant"] = 1  # cohérent avec la logique du modèle

        dpe_pred = model_dpe.predict(df)[0]
        if preproc_conso is not None:
            X_trans = preproc_conso.transform(df)
            conso_pred = model_conso.predict(X_trans)[0]
        else:
            conso_pred = model_conso.predict(df)[0]

        return {"DPE": str(dpe_pred), "Conso_kWh_m2": round(float(conso_pred), 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur GET prédiction : {e}")

@app.post("/refresh_data")
def refresh_data():
    """
    Met à jour le dataset local en récupérant les DPE (existants + neufs)
    plus récents que la dernière date locale, depuis les APIs ADEME.
    """
    import pyproj

    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="Dataset local introuvable.")

    # --- Lecture dataset local ---
    try:
        df_local = pd.read_csv(DATA_PATH)
        last_date = pd.to_datetime(df_local["date_reception_dpe"], errors="coerce").max()
        last_date_str = last_date.strftime("%Y-%m-%d")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lecture dataset local : {e}")

    st_cols = list(df_local.columns)  # Schéma de référence
    print(f"[INFO] {len(st_cols)} colonnes attendues dans le dataset final.")

    # --- Paramètres communs API ADEME ---
    DEPT = "73"
    PAGE_SIZE = 1200
    ADEME_ENDPOINTS = {
        "existants": "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines",
        "neufs": "https://data.ademe.fr/data-fair/api/v1/datasets/dpe02neuf/lines"
    }

    new_frames = []
    total_new_rows = 0

    for label, url in ADEME_ENDPOINTS.items():
        print(f"\n--- Téléchargement {label.upper()} ---")
        params = {
            "q": f"{DEPT}*",
            "q_fields": "code_postal_ban",
            "qs": f"date_reception_dpe:[{last_date_str} TO *]",
            "size": PAGE_SIZE,
            "sort": "date_reception_dpe"
        }

        try:
            r = requests.get(url, params=params, timeout=120)
            r.raise_for_status()
            data = r.json()
            results = data.get("results", [])
            if not results:
                print(f"[INFO] Aucun nouveau DPE pour {label}")
                continue
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur API ADEME ({label}) : {e}")

        df_new = pd.DataFrame(results)
        df_new["Logement"] = "Ancien" if label == "existants" else "Neuf"
        total_new_rows += len(df_new)

        # --- Harmonisation des colonnes ---
        # Garde uniquement les colonnes déjà présentes dans le dataset local
        df_new = df_new.reindex(columns=st_cols, fill_value=pd.NA)
        new_frames.append(df_new)
        print(f"[INFO] {len(df_new)} nouvelles lignes récupérées pour {label}.")

    # --- Vérification ---
    if not new_frames:
        return {"status": "no_update", "message": "Aucune donnée nouvelle détectée."}

    df_new_all = pd.concat(new_frames, ignore_index=True)

    # --- Fusion & Sauvegarde ---
    df_final = pd.concat([df_local, df_new_all], ignore_index=True)
    df_final.to_csv(DATA_PATH, index=False)

    return {
        "status": "ok",
        "new_rows": int(total_new_rows),
        "updated_until": str(df_final["date_reception_dpe"].max())[:10]
    }
# ------------------------------------------------------------
# 🚀 Run local
# ------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
