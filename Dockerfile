# ===========================================================
# 🐳 Dockerfile de production pour Streamlit (Koyeb)
# ===========================================================
FROM python:3.12-slim

# Éviter les fichiers .pyc et activer stdout direct
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installer dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt huggingface_hub

# Copier le code de l’application (sans data/models)
COPY Scripts/app /app/Scripts/app

# Créer les dossiers persistants pour données et modèles
VOLUME ["/app/data", "/app/models"]

# Copier le script d’amorçage Hugging Face
COPY init_assets.py /app/init_assets.py

# Exposer le port Streamlit
EXPOSE 8501

# Télécharger les fichiers Hugging Face au démarrage,
# puis lancer l'application Streamlit
CMD ["bash", "-c", "python init_assets.py && streamlit run Scripts/app/main.py --server.address=0.0.0.0 --server.port=8501"]
