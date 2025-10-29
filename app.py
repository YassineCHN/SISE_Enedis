# app.py
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
import pandas as pd
import joblib
import os

app = Flask(__name__)
swagger = Swagger(app)

# 📦 Chemin du modèle (entraîné avec EXACTEMENT les 15 features ci-dessous)
MODEL_PATH = os.getenv("MODEL_PATH", "./Modèle/pipeline.pkl")
modelClassification = joblib.load(MODEL_PATH)



@app.route("/", methods=["GET"])
def home():
    return "Bienvenue sur l'API de prévision de consommation énergétique ."

@app.route("/data", methods=["GET"])
@swag_from({
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 1,
            'description': "Numéro de la page à récupérer"
        },
        {
            'name': 'size',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 10,
            'description': "Nombre d'éléments par page"
        }
    ],
    'responses': {
        200: {
            'description': "Récupérer les données paginées",
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'page': {'type': 'integer'},
                    'size': {'type': 'integer'},
                    'total_pages': {'type': 'integer'},
                    'data': {
                        'type': 'object',
                        'additionalProperties': {
                            'type': 'array',
                            'items': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def get_data():
    # Lecture des données
    df = pd.read_csv("./data/donnees_dpe_rhone_clean.csv")

    # Récupération des paramètres de pagination
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=10, type=int)

    # Calcul de l'index de début et de fin
    start = (page - 1) * size
    end = start + size

    # Nombre total de pages
    total_pages = (len(df) + size - 1) // size

    # Extraction des données pour la page demandée
    paginated_data = df[start:end].to_dict(orient="list")

    # Retour des données paginées
    return jsonify({
        'message': "Données récupérées avec succès",
        'page': page,
        'size': size,
        'total_pages': total_pages,
        'data': paginated_data
    })


# ✅ Variables explicatives (ordre figé)
ls_variables_explicatives = [
    'conso_5_usages_par_m2_ep',
    'emission_ges_5_usages_par_m2',
    'conso_5_usages_par_m2_ef',
    'conso_chauffage_ep',
    'emission_ges_chauffage',
    'cout_chauffage',
    'besoin_ecs',
    'surface_habitable_logement',
    'cout_total_5_usages',
    'conso_5_usages_ef_energie_n1',
    'conso_ecs_ep',
    'conso_eclairage_ef',
    'type_energie_principale_chauffage',  # catégorielle (string)
    'conso_chauffage_ef',
    'annee_construction'
]

# Colonnes numériques = toutes sauf l'énergie principale (catégorielle)
num_cols = [c for c in ls_variables_explicatives if c != 'type_energie_principale_chauffage']

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "status": "ok",
        "message": "API SISE Enedis – classification",
        "model_path": MODEL_PATH,
        "expected_features": ls_variables_explicatives
    })

@app.route("/classification", methods=["POST"])
@swag_from({
    "tags": ["Classification"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "parameters": [{
        "name": "body",
        "in": "body",
        "required": True,
        "schema": {
            "type": "object",
            "properties": {
                "conso_5_usages_par_m2_ep": {"type": "number", "description": "Conso 5 usages/m² (énergie primaire) – kWh/m²"},
                "emission_ges_5_usages_par_m2": {"type": "number", "description": "GES 5 usages/m² – kgCO2/m²"},
                "conso_5_usages_par_m2_ef": {"type": "number", "description": "Conso 5 usages/m² (énergie finale) – kWh/m²"},
                "conso_chauffage_ep": {"type": "number", "description": "Conso chauffage (énergie primaire) – kWh"},
                "emission_ges_chauffage": {"type": "number", "description": "GES chauffage – kgCO2"},
                "cout_chauffage": {"type": "number", "description": "Coût chauffage – €"},
                "besoin_ecs": {"type": "number", "description": "Besoin ECS – kWh"},
                "surface_habitable_logement": {"type": "number", "description": "Surface habitable – m²"},
                "cout_total_5_usages": {"type": "number", "description": "Coût total 5 usages – €"},
                "conso_5_usages_ef_energie_n1": {"type": "number", "description": "Conso 5 usages (énergie finale) – énergie n°1 – kWh"},
                "conso_ecs_ep": {"type": "number", "description": "Conso ECS (énergie primaire) – kWh"},
                "conso_eclairage_ef": {"type": "number", "description": "Conso éclairage (énergie finale) – kWh"},
                "type_energie_principale_chauffage": {
                    "type": "string",
                    "description": "Type d'énergie principale du chauffage",
                    "enum": [
                        "Électricité", "Gaz naturel", "Charbon", "Bois – Bûches",
                        "Fioul domestique", "Réseau de Chauffage urbain",
                        "Bois – Granulés (pellets) ou briquettes", "Bois – Plaquettes d’industrie",
                        "GPL", "Bois – Plaquettes forestières", "Propane",
                        "Électricité d'origine renouvelable utilisée dans le bâtiment"
                    ]
                },
                "conso_chauffage_ef": {"type": "number", "description": "Conso chauffage (énergie finale) – kWh"},
                "annee_construction": {"type": "integer", "description": "Année de construction du logement"}
            },
            "required": ls_variables_explicatives,
            "example": {
                "conso_5_usages_par_m2_ep": 250,
                "emission_ges_5_usages_par_m2": 40,
                "conso_5_usages_par_m2_ef": 210,
                "conso_chauffage_ep": 8000,
                "emission_ges_chauffage": 2000,
                "cout_chauffage": 900,
                "besoin_ecs": 2500,
                "surface_habitable_logement": 85,
                "cout_total_5_usages": 1400,
                "conso_5_usages_ef_energie_n1": 7000,
                "conso_ecs_ep": 1800,
                "conso_eclairage_ef": 450,
                "type_energie_principale_chauffage": "Électricité",
                "conso_chauffage_ef": 6200,
                "annee_construction": 1998
            }
        }
    }],
    "responses": {
        200: {
            "description": "Résultat de la classification",
            "schema": {"type": "object", "properties": {"classification": {"type": "string"}}}
        },
        400: {"description": "Requête invalide (champs manquants / non numériques)"},
        500: {"description": "Erreur interne (modèle / prédiction)"}
    }
})
def classification():
    # 1) Lire le JSON
    data = request.get_json(force=True, silent=False)
    if not isinstance(data, dict):
        return jsonify({"error": "Le corps de la requête doit être un objet JSON."}), 400

    # 2) Vérifier les champs manquants
    missing = [c for c in ls_variables_explicatives if c not in data]
    if missing:
        return jsonify({"error": "Variables manquantes.", "missing_features": missing}), 400

    # 3) Construire X (ordre strict) et caster les colonnes numériques
    X = pd.DataFrame({c: [data.get(c)] for c in ls_variables_explicatives})
    for c in num_cols:
        X[c] = pd.to_numeric(X[c], errors="coerce")

    # 4) Contrôle NaN (numériques)
    if X[num_cols].isna().any().any():
        return jsonify({
            "error": "Certaines variables numériques sont invalides (non numériques ou nulles).",
            "invalid_numeric_features": X[num_cols].columns[X[num_cols].isna().any()].tolist()
        }), 400

    # 5) Prédiction
    try:
        y_pred = modelClassification.predict(X)[0]
    except Exception as e:
        return jsonify({"error": f"Erreur modèle: {str(e)}"}), 500

    return jsonify({"classification": str(y_pred)}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    # ⚠️ En production: debug=False
    app.run(host="0.0.0.0", port=port, debug=True)
