# 🚀 Installation et Utilisation - Banking Transactions API

Guide complet pour installer et utiliser l'API de transactions bancaires.

---

## 📋 Prérequis

- **Python 3.12+** installé sur votre système
- **pip** (gestionnaire de paquets Python)
- **Git** (pour cloner le projet)

---

## 📥 Installation

### Option 1: Installation en mode développement (Recommandé)

```bash
# 1. Cloner le dépôt
git clone https://github.com/masiszovikoglu/projet_python_2_mba.git
cd projet_python_2_mba

# 2. Créer un environnement virtuel
python -m venv venv

# 3. Activer l'environnement virtuel
# Sur Windows:
.\venv\Scripts\Activate.ps1
# Sur Linux/Mac:
source venv/bin/activate

# 4. Installer le package en mode éditable avec dépendances de développement
pip install -e ".[dev]"

# 5. Placer votre fichier de données
# Télécharger: https://www.kaggle.com/datasets/ealaxi/banksim1
# Placer le fichier bs140513_032310.csv dans le dossier data/
```

### Option 2: Installation en mode production

```bash
# 1. Cloner et naviguer vers le projet
git clone https://github.com/masiszovikoglu/projet_python_2_mba.git
cd projet_python_2_mba

# 2. Créer et activer l'environnement virtuel
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac

# 3. Installer le package
pip install .

# 4. Placer votre fichier de données dans data/
```

### Option 3: Installation depuis le wheel/tarball

```bash
# Si vous avez un fichier de distribution
pip install banking-transactions-api-1.0.0.tar.gz

# Ou depuis un wheel
pip install banking-transactions-api-1.0.0-py3-none-any.whl
```

---

## ✅ Vérification de l'Installation

```bash
# Vérifier que le package est installé
pip show banking-transactions-api

# Tester l'import du module
python -c "import banking_api; print(f'✅ Version: {banking_api.__version__}')"

# Vérifier que la commande est disponible
banking-api --help  # (Démarre le serveur)
```

**Sortie attendue:**
```
Name: banking-transactions-api
Version: 1.0.0
Summary: API REST pour l'exposition des données de transactions bancaires
```

---

## 🚀 Démarrage de l'API

### Méthode 1: Via la commande console (Recommandé)

```bash
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Démarrer le serveur API
banking-api
```

### Méthode 2: Via uvicorn directement

```bash
# Mode développement avec auto-reload
uvicorn banking_api.main:app --reload --host 0.0.0.0 --port 8000

# Mode production
uvicorn banking_api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Méthode 3: Via Python

```python
from banking_api.main import start_server

# Démarre le serveur
start_server()
```

**Sortie attendue:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 📡 Accéder à l'API

### Interface Interactive (Swagger UI)

Ouvrez votre navigateur et accédez à:

```
http://localhost:8000/docs
```

Vous verrez l'interface Swagger avec tous les endpoints disponibles et pourrez tester l'API interactivement.

### Documentation Alternative (ReDoc)

```
http://localhost:8000/redoc
```

### Vérifier le Statut

```bash
# Vérifier que l'API fonctionne
curl http://localhost:8000/

# Vérifier la santé du système
curl http://localhost:8000/api/system/health
```

**Réponse attendue:**
```json
{
  "status": "ok",
  "message": "Banking Transactions API v1.0.0",
  "documentation": "/docs"
}
```

---

## 🔍 Exemples d'Utilisation

### 1. Lister les transactions (Python)

```python
import requests

# Récupérer les 10 premières transactions
response = requests.get("http://localhost:8000/api/transactions", params={
    "skip": 0,
    "limit": 10
})

data = response.json()
print(f"Total transactions: {data['total']}")
print(f"Transactions récupérées: {len(data['transactions'])}")
```

### 2. Obtenir une transaction spécifique

```bash
curl http://localhost:8000/api/transactions/7475327
```

### 3. Rechercher des transactions frauduleuses

```python
import requests

response = requests.get("http://localhost:8000/api/fraud/summary")
fraud_data = response.json()

print(f"Transactions frauduleuses: {fraud_data['fraud_count']}")
print(f"Taux de fraude: {fraud_data['fraud_rate']:.2%}")
```

### 4. Obtenir des statistiques

```bash
# Statistiques globales
curl http://localhost:8000/api/stats/overview

# Distribution des montants
curl http://localhost:8000/api/stats/amount-distribution?bins_count=10
```

### 5. Prédiction de fraude

```python
import requests

prediction_request = {
    "amount": 500.00,
    "merchant_id": 123456,
    "use_chip": "Online Transaction",
    "merchant_state": "NY"
}

response = requests.post(
    "http://localhost:8000/api/fraud/predict",
    json=prediction_request
)

result = response.json()
print(f"Probabilité de fraude: {result['fraud_probability']:.2%}")
print(f"Niveau de risque: {result['risk_level']}")
```

### 6. Obtenir le profil d'un client

```bash
curl "http://localhost:8000/api/customers/profile?customer_id=1231006815"
```

---

## 🛠️ Configuration

### Variables d'Environnement

Créez un fichier `.env` à la racine du projet:

```env
# Chemin vers le fichier de données
DATA_PATH=data/bs140513_032310.csv

# Configuration du serveur
API_HOST=0.0.0.0
API_PORT=8000

# Pagination
MAX_PAGE_SIZE=1000
DEFAULT_PAGE_SIZE=100
```

### Charger les variables d'environnement

```bash
# Sur Windows PowerShell
$env:DATA_PATH="data/bs140513_032310.csv"

# Sur Linux/Mac
export DATA_PATH="data/bs140513_032310.csv"
```

---

## 🧪 Exécuter les Tests

```bash
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Exécuter tous les tests avec couverture
pytest tests/ --cov=src/banking_api --cov-report=html

# Exécuter un fichier de test spécifique
pytest tests/test_transactions_routes.py -v

# Voir le rapport de couverture
# Ouvrir: htmlcov/index.html dans votre navigateur
```

---

## 📚 Routes API Disponibles

### 🔄 Transactions (8 routes)
- `GET /api/transactions` - Liste paginée
- `GET /api/transactions/{id}` - Détails d'une transaction
- `POST /api/transactions/search` - Recherche multicritère
- `GET /api/transactions/types` - Types disponibles
- `GET /api/transactions/recent` - Transactions récentes
- `GET /api/transactions/by-customer` - Par client
- `GET /api/transactions/to-merchant` - Par commerçant
- `DELETE /api/transactions/{id}` - Supprimer (test)

### 👥 Clients (3 routes)
- `GET /api/customers` - Liste des clients
- `GET /api/customers/profile` - Profil client
- `GET /api/customers/top` - Meilleurs clients

### 🚨 Fraude (3 routes)
- `GET /api/fraud/summary` - Résumé de la fraude
- `GET /api/fraud/by-merchant` - Fraude par commerçant
- `POST /api/fraud/predict` - Prédiction de fraude

### 📊 Statistiques (4 routes)
- `GET /api/stats/overview` - Vue d'ensemble
- `GET /api/stats/amount-distribution` - Distribution montants
- `GET /api/stats/by-chip` - Statistiques par type
- `GET /api/stats/daily` - Statistiques journalières

### ⚙️ Système (2 routes)
- `GET /api/system/health` - État du système
- `GET /api/system/metadata` - Métadonnées

---

## 🔧 Dépannage

### Problème: Module non trouvé

```bash
# Solution: Réinstaller le package
pip install -e .
```

### Problème: Port 8000 déjà utilisé

```bash
# Solution: Utiliser un autre port
uvicorn banking_api.main:app --port 8080
```

### Problème: Fichier de données non trouvé

```bash
# Solution: Vérifier le chemin
python -c "from banking_api.config import Settings; print(Settings().DATA_PATH)"

# Définir la variable d'environnement
$env:DATA_PATH="C:\chemin\complet\vers\bs140513_032310.csv"
```

### Problème: Erreur d'import pandas/numpy

```bash
# Solution: Réinstaller les dépendances
pip install --upgrade pandas numpy
```

---

## 📦 Désinstallation

```bash
# Désinstaller le package
pip uninstall banking-transactions-api

# Supprimer l'environnement virtuel
deactivate
rm -rf venv  # Linux/Mac
Remove-Item -Recurse -Force venv  # Windows PowerShell
```

---

## 📄 Licence

Ce projet est développé dans le cadre du programme ESG MBA - Python 2.

---

## 🆘 Support

Pour toute question ou problème:
1. Consultez la documentation interactive: http://localhost:8000/docs
2. Vérifiez les logs du serveur
3. Consultez le README.md du projet
4. Exécutez les tests pour vérifier l'installation

---

**✨ Votre API est maintenant prête à l'emploi !**
