# ===========================================================
# 🐳 Dockerfile combiné : FastAPI + Streamlit + Hugging Face
# ===========================================================
FROM python:3.12-slim

# Empêcher création de .pyc et forcer sortie stdout immédiate
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installer dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 && rm -rf /var/lib/apt/lists/*

# Copier les dépendances Python
COPY requirements.txt .

# Installer toutes les dépendances nécessaires à Streamlit + FastAPI + modèles
RUN pip install --no-cache-dir -r requirements.txt \
    fastapi uvicorn streamlit joblib pandas scikit-learn plotly huggingface_hub requests

# Copier tout le projet (API, scripts, data, models, etc.)
COPY . .

# Créer les dossiers persistants
VOLUME ["/app/data", "/app/models"]

# Exposer les deux ports
EXPOSE 8000
EXPOSE 8501

# Commande de démarrage :
# - Télécharge les fichiers depuis Hugging Face (init_assets.py)
# - Lance l'API (port 8000)
# - Lance Streamlit (port 8501)
CMD ["bash", "-c", "python init_assets.py && \
    uvicorn api.main:app --host 0.0.0.0 --port 8000 & \
    streamlit run Scripts/app/main.py --server.address=0.0.0.0 --server.port=8501"]
