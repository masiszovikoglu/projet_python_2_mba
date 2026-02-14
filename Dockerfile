# Dockerfile pour Banking Transactions API
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY pyproject.toml setup.py MANIFEST.in ./
COPY README.md ./

# Copier le code source
COPY src/ ./src/

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Créer un répertoire pour les données
RUN mkdir -p /app/data

# Exposer le port de l'API
EXPOSE 8000

# Variables d'environnement par défaut
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV DATA_PATH=/app/data/transactions_data.csv

# Commande de démarrage
CMD ["uvicorn", "banking_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
