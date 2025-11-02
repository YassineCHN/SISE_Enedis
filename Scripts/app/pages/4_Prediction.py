# ============================================================
# 🧩 PAGE 4 — PREDICTION
# France Énergie - Diagnostic et Éligibilité MaPrimeRénov’
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib, os, glob
import requests

st.set_page_config(page_title="Prédictions", page_icon="⚡", layout="wide")

st.title("⚡ Simulation de performance énergétique")
st.markdown(
    "Remplissez les caractéristiques de votre logement pour obtenir une estimation du DPE, "
    "de l’éligibilité MaPrimeRénov’ et de la consommation énergétique."
)

# ============================================================
# 🔁 Chargement des modèles
# ============================================================

@st.cache_resource
def load_models():
    models_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "models")
    models_dir = os.path.abspath(models_dir)

    def pick(path_pattern, fallback_pattern):
        latest = os.path.join(models_dir, path_pattern)
        if os.path.exists(latest):
            return latest
        candidates = sorted(glob.glob(os.path.join(models_dir, fallback_pattern)),
                            key=os.path.getmtime, reverse=True)
        return candidates[0] if candidates else None

    dpe_path = pick("model_DPE_latest.pkl", "model_DPE_*.pkl")
    mpr_path = pick("model_MPR_latest.pkl", "model_MPR_*.pkl")
    conso_path = pick("model_CONSO_*.pkl", "model_CONSO_*.pkl")
    preproc_conso_path = os.path.join(models_dir, "preprocessor_conso.pkl")

    models = {}
    for key, path in {
        "dpe": dpe_path,
        "mpr": mpr_path,
        "conso": conso_path,
        "preproc_conso": preproc_conso_path
    }.items():
        if path and os.path.exists(path):
            models[key] = joblib.load(path)
        else:
            st.info(f"ℹ️ Modèle non chargé : {path}")
            models[key] = None
    return models


# ============================================================
# 🧠 Fonction d’interprétation DPE
# ============================================================

def dpe_label_from_model(model_pipeline, X_input):
    """Retourne (label_str, y_raw, mapping_dict)"""
    if model_pipeline is None:
        return None, None, {}

    y_raw = model_pipeline.predict(X_input)[0]

    classes = None
    try:
        classes = model_pipeline.named_steps["model"].classes_
    except Exception:
        pass

    # Cas 1 : modèle entraîné directement sur les lettres
    if classes is not None and all(isinstance(c, str) for c in classes):
        label = str(y_raw)
        mapping = {c: c for c in classes}
        return label, y_raw, mapping

    # Cas 2 : modèle numérique (sécurité)
    letters = ["G", "F", "E", "D", "C", "B", "A"]  # de plus mauvais à meilleur
    try:
        if classes is None:
            classes_sorted = list(range(7))
        else:
            classes_sorted = sorted(list(classes))
        mapping = {cls: letters[i] for i, cls in enumerate(classes_sorted)}
        label = mapping.get(y_raw)
        return label, y_raw, mapping
    except Exception:
        return None, y_raw, {}


# ============================================================
# 🔍 Extraction du vocabulaire attendu
# ============================================================

def get_expected_schema(pipe):
    if pipe is None:
        return {"num": [], "cat": [], "categories": {}}
    pre = pipe.named_steps["preprocess"]
    num_features = pre.transformers_[0][2]
    cat_features = pre.transformers_[1][2]
    enc = pre.named_transformers_["cat"].named_steps["encoder"]
    cats = enc.categories_
    categories_by_feature = {feat: list(cats[i]) for i, feat in enumerate(cat_features)}
    return {"num": list(num_features), "cat": list(cat_features), "categories": categories_by_feature}

def normalize_categories(X_in, expected_schema):
    """Corrige les petites différences de casse ou tirets."""
    X = X_in.copy()
    for feat, vals in expected_schema["categories"].items():
        if feat in X.columns and isinstance(X.iloc[0][feat], str):
            val = X.iloc[0][feat].strip()
            match = next(
                (v for v in vals if v.lower().replace("-", "–") == val.lower().replace("-", "–")),
                val
            )
            X.at[0, feat] = match
    return X


# ============================================================
# 📦 Chargement initial
# ============================================================

models = load_models()
model_dpe = models["dpe"]
model_mpr = models["mpr"]
model_conso = models["conso"]
preproc_conso = models["preproc_conso"]

schema_dpe = get_expected_schema(model_dpe)

# ============================================================
# 🏠 Formulaire utilisateur
# ============================================================

st.subheader("🧱 Caractéristiques du logement")

col1, col2 = st.columns(2)

with col1:
    annee_construction = st.number_input("Année de construction", min_value=1800, max_value=2025, value=1990)
    surface = st.number_input("Surface habitable (m²)", min_value=10, max_value=500, value=80)
    type_batiment = st.selectbox("Type de bâtiment", ["appartement", "maison"])
    classe_inertie = st.selectbox("Classe d’inertie du bâtiment", ["Lourde", "Légère", "Moyenne", "Très lourde"])
    qualite_murs = st.selectbox("Qualité d’isolation des murs", ["bonne", "insuffisante", "moyenne", "très bonne"])

with col2:
    type_energie = st.selectbox("Type d’énergie principale du chauffage", [
        "Bois – Bûches",
        "Bois – Granulés (pellets) ou briquettes",
        "Bois – Plaquettes d’industrie",
        "Bois – Plaquettes forestières",
        "Butane",
        "Charbon",
        "Fioul domestique",
        "GPL",
        "Gaz naturel",
        "Propane",
        "Réseau de Chauffage urbain",
        "Électricité",
        "Électricité d'origine renouvelable utilisée dans le bâtiment"
    ])
    qualite_menuiseries = st.selectbox("Qualité d’isolation des menuiseries", ["bonne", "insuffisante", "moyenne", "très bonne"])
    classe_altitude = st.selectbox("Classe d’altitude", ["400-800m", "Non affecté", "inférieur à 400m", "supérieur à 800m"])
    logement_traversant = st.selectbox("Logement traversant", ["oui", "non"])

predict_btn = st.button("⚡ Lancer la prédiction", use_container_width=True, type="primary")

# ============================================================
# 🔮 Prédictions
# ============================================================

if predict_btn:
    X_input = pd.DataFrame([{
        "annee_construction": annee_construction,
        "surface_habitable_logement": surface,
        "type_batiment": type_batiment,
        "type_energie_principale_chauffage": type_energie,
        "classe_inertie_batiment": classe_inertie,
        "qualite_isolation_murs": qualite_murs,
        "qualite_isolation_menuiseries": qualite_menuiseries,
        "classe_altitude": classe_altitude,
        "logement_traversant": 1 if logement_traversant == "oui" else 0
    }])

    X_input = normalize_categories(X_input, schema_dpe)

    st.markdown("#### 📋 Données saisies :")
    st.dataframe(X_input)

    etiquette = None
    y_raw_dpe = None
    y_pred_mpr = None
    y_pred_conso = None
    dpe_map = {}

    # --- DPE ---
    try:
        etiquette, y_raw_dpe, dpe_map = dpe_label_from_model(model_dpe, X_input)
        if etiquette:
            st.metric("Étiquette DPE prédite", etiquette)
        else:
            st.error(f"⚠️ Valeur DPE inattendue ({y_raw_dpe}).")
            st.metric("Étiquette DPE prédite", "—")
    except Exception as e:
        st.error(f"Erreur DPE : {e}")

    # --- Jauge visuelle ---
    if etiquette in list("ABCDEFG"):
        colors = {"A":"#00A651","B":"#6BBE45","C":"#F1E600","D":"#F9A61A",
                  "E":"#F36F21","F":"#ED1C24","G":"#A31722"}
        html = "<div style='display:flex;gap:4px;margin:10px 0;'>"
        for lab in list("ABCDEFG"):
            html += f"<div style='flex:1;text-align:center;background:{colors[lab]};color:white;padding:6px;border-radius:4px;font-weight:700;opacity:{'1' if lab==etiquette else '0.4'}'>{lab}</div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("Aucune étiquette DPE prédite pour cette configuration.")

    # --- MPR ---
    try:
        y_pred_mpr = model_mpr.predict(X_input)[0]
        eligibilite = "✅ Oui" if y_pred_mpr == 1 else "❌ Non"
        st.metric("Éligible MaPrimeRénov’", eligibilite)
    except Exception as e:
        st.error(f"Erreur MPR : {e}")

    # --- Consommation ---
    try:
        X_trans = preproc_conso.transform(X_input)
        y_pred_conso = model_conso.predict(X_trans)[0]
        st.metric("Consommation estimée", f"{y_pred_conso:,.0f} kWh/m²/an")
    except Exception as e:
        st.error(f"Erreur régression : {e}")

    # --- Texte explicatif ---
    if etiquette:
        desc = {
            "A": "Excellente performance énergétique 💚",
            "B": "Très bonne performance énergétique 💚",
            "C": "Bonne performance énergétique 💛",
            "D": "Performance moyenne 🟧",
            "E": "Consommation élevée 🟥",
            "F": "Très forte consommation 🔴",
            "G": "Consommation excessive 🚨"
        }.get(etiquette, "")
        st.markdown(f"**{desc}**")

    if 'y_pred_mpr' in locals():
        st.markdown("_" + (
            "Ce logement est **éligible** à MaPrimeRénov’ 🎯"
            if y_pred_mpr == 1
            else "Ce logement **n’est pas éligible** à MaPrimeRénov’ car sa classe DPE est supérieure à D."
        ) + "_")

    # ============================================================
    # 🧩 Mode Debug
    # ============================================================
    debug_mode = st.toggle("🧠 Activer le mode debug")

    if debug_mode:
        st.markdown("---")
        st.subheader("🔍 Détails techniques (Debug)")
        st.write("**Valeur brute DPE (y_raw)** :", y_raw_dpe)
        st.write("**Mapping classes → lettres** :", dpe_map)
        st.write("**Étiquette DPE finale** :", etiquette)
        st.write("**Prédiction MPR (0=Non,1=Oui)** :", int(y_pred_mpr) if y_pred_mpr is not None else None)
        st.write("**Prédiction consommation (kWh/m²/an)** :", round(float(y_pred_conso), 2) if y_pred_conso is not None else None)

        # 🔎 Vérification des catégories
        if schema_dpe["categories"]:
            st.markdown("**Vérification des catégories connues (DPE)**")
            for feat in schema_dpe["cat"]:
                vals = schema_dpe["categories"].get(feat, [])
                val_in = X_input.iloc[0][feat]
                if val_in not in vals:
                    st.warning(f"⚠️ Valeur hors vocabulaire pour `{feat}` : `{val_in}`")
                else:
                    st.success(f"✅ `{feat}` ok : {val_in}")
