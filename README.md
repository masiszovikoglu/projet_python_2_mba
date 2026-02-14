# Banking Transactions API

[![CI/CD Pipeline](https://github.com/masiszovikoglu/MBA-2---Python---Projet-Exposition-de-donn-es-sous-la-forme-d-une-API/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/masiszovikoglu/MBA-2---Python---Projet-Exposition-de-donn-es-sous-la-forme-d-une-API/actions)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)

API REST complète pour l'exposition et la manipulation des données de transactions bancaires. Développé dans le cadre du MBA 2 - ESG, ce projet implémente 20 endpoints pour la consultation, l'analyse statistique, la détection de fraude et la gestion des clients.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [API Documentation](#-api-documentation)
- [Tests](#-tests)
- [Docker](#-docker)
- [Structure du projet](#-structure-du-projet)

## 🚀 Fonctionnalités

### Transactions (8 endpoints)
- ✅ Liste paginée avec filtres (type, fraude, montant)
- ✅ Détails d'une transaction par ID
- ✅ Recherche multicritère
- ✅ Types de transactions disponibles
- ✅ Transactions récentes
- ✅ Suppression (mode test)
- ✅ Transactions par client (émetteur)
- ✅ Transactions vers un client (destinataire)

### Statistiques (4 endpoints)
- ✅ Vue d'ensemble globale
- ✅ Distribution des montants
- ✅ Statistiques par type de transaction
- ✅ Statistiques quotidiennes

### Détection de fraude (3 endpoints)
- ✅ Résumé des fraudes
- ✅ Taux de fraude par type
- ✅ Prédiction de fraude (scoring heuristique)

### Clients (3 endpoints)
- ✅ Liste paginée des clients
- ✅ Profil client détaillé
- ✅ Top clients par volume

### Administration (2 endpoints)
- ✅ Santé du système
- ✅ Métadonnées de l'API

## 🏗 Architecture

Le projet suit une architecture en couches :

```
├── models.py          # Modèles Pydantic (validation)
├── services/          # Logique métier
│   ├── transactions_service.py
│   ├── stats_service.py
│   ├── fraud_detection_service.py
│   ├── customer_service.py
│   └── system_service.py
├── routes/            # Endpoints FastAPI
│   ├── transactions.py
│   ├── stats.py
│   ├── fraud.py
│   ├── customers.py
│   └── system.py
├── data_manager.py    # Gestion des données (singleton)
├── config.py          # Configuration
└── main.py            # Application FastAPI
```

## 📦 Installation

### Prérequis

- Python 3.12+
- pip

### Installation standard

```powershell
# Cloner le dépôt
git clone https://github.com/masiszovikoglu/MBA-2---Python---Projet-Exposition-de-donn-es-sous-la-forme-d-une-API.git
cd MBA-2---Python---Projet-Exposition-de-donn-es-sous-la-forme-d-une-API-1

# Créer un environnement virtuel
python -m venv venv
.\venv\Scripts\Activate.ps1

# Installer le package
pip install -e .

# Installer les dépendances de développement
pip install -e ".[dev]"
```

### Préparation des données

1. Télécharger le dataset depuis Kaggle :
   https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets/data

2. Placer le fichier `transactions_data.csv` dans le dossier `data/` :
   ```powershell
   mkdir data
   # Copier transactions_data.csv dans data/
   ```

## 🎯 Utilisation

### Démarrer l'API

```powershell
# Via uvicorn directement
uvicorn banking_api.main:app --reload --host 0.0.0.0 --port 8000

# Via la commande installée
banking-api

# Avec variables d'environnement
$env:DATA_PATH="data/transactions_data.csv"; uvicorn banking_api.main:app --reload
```

L'API sera accessible sur : http://localhost:8000

### Documentation interactive

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 📚 API Documentation

### Exemples d'utilisation

#### Récupérer des transactions

```powershell
# Toutes les transactions
curl http://localhost:8000/api/transactions?page=1&limit=10

# Filtrer par type
curl http://localhost:8000/api/transactions?type=TRANSFER

# Filtrer les fraudes
curl http://localhost:8000/api/transactions?isFraud=1
```

#### Statistiques

```powershell
# Vue d'ensemble
curl http://localhost:8000/api/stats/overview

# Distribution des montants
curl http://localhost:8000/api/stats/amount-distribution?bins=10
```

## 🧪 Tests

### Tests unitaires (pytest)

```powershell
# Exécuter tous les tests
pytest tests/ -v

# Avec couverture
pytest tests/ -v --cov=src/banking_api --cov-report=html
```

### Tests features (unittest)

```powershell
# Tests d'intégration
python -m unittest discover -s tests -p "test_features.py" -v
```

## 🐋 Docker

### Construction et exécution

```powershell
# Construction
docker build -t banking-api:latest .

# Exécution
docker run -d -p 8000:8000 -v ${PWD}/data:/app/data banking-api:latest

# Avec Docker Compose
docker-compose up -d
```

## 📁 Structure du projet

```
MBA-2---Python---Projet-Exposition-de-donn-es-sous-la-forme-d-une-API-1/
├── src/banking_api/        # Code source
├── tests/                  # Tests
├── data/                   # Données CSV
├── pyproject.toml         # Configuration
├── setup.py               # Setup
├── Dockerfile             # Image Docker
└── README.md              # Documentation
```

## 🔍 Qualité du code

- ✅ **PEP8** : Conformité flake8
- ✅ **Typing** : Types Python complets
- ✅ **Documentation** : NumPy docstring style
- ✅ **Tests** : Couverture ≥85%

## 👥 Auteurs

**Groupe MBA 2 - Python**
- Projet : API Transactions Bancaires
- Formateur : Rakib SHEIKH
- Date : Décembre 2025