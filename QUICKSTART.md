# 🚀 Guide de Démarrage Rapide

## Prérequis installés ✓
- Python 3.12+
- Git

## 📥 Étape 1 : Extraire les données Kaggle

Vous avez téléchargé l'archive. Maintenant :

```powershell
# Extraire le fichier transactions_data.csv dans le dossier data/
# Si c'est un ZIP :
Expand-Archive -Path "chemin\vers\archive.zip" -DestinationPath ".\data" -Force

# Vérifier que le fichier est présent
Test-Path ".\data\transactions_data.csv"
# Devrait retourner: True
```

## 🎯 Étape 2 : Installation et démarrage (MÉTHODE FACILE)

Utilisez le script automatisé :

```powershell
# Lancer l'installation et démarrer l'API en une commande
.\setup_and_run.ps1
```

Ce script va :
1. ✓ Vérifier Python
2. ✓ Créer l'environnement virtuel
3. ✓ Installer toutes les dépendances
4. ✓ Vérifier les données
5. ✓ Démarrer l'API sur http://localhost:8000

## 🔧 Étape 2 BIS : Installation manuelle (si besoin)

```powershell
# 1. Créer l'environnement virtuel
python -m venv venv

# 2. Activer l'environnement
.\venv\Scripts\Activate.ps1

# 3. Installer le package
pip install -e .

# 4. Installer les dépendances de dev
pip install -e ".[dev]"

# 5. Démarrer l'API
uvicorn banking_api.main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Étape 3 : Tester l'API

L'API est accessible sur : **http://localhost:8000**

### Documentation interactive :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

### Test rapide dans PowerShell :

```powershell
# Test de santé
curl http://localhost:8000/api/system/health

# Liste des transactions
curl http://localhost:8000/api/transactions?page=1&limit=5

# Statistiques globales
curl http://localhost:8000/api/stats/overview
```

## 🧪 Étape 4 : Lancer les tests

### Tests complets automatisés :

```powershell
.\quick_test.ps1
```

### Tests manuels :

```powershell
# Tests pytest avec couverture
pytest tests/ -v --cov=src/banking_api --cov-report=html

# Tests unittest
python -m unittest discover -s tests -p "test_features.py" -v

# Vérifier flake8
flake8 src/banking_api/

# Vérifier mypy
mypy src/banking_api/ --config-file mypy.ini
```

## 📦 Étape 5 : Construire le package

```powershell
# Construction automatisée
.\build_package.ps1

# Les fichiers seront dans dist/
```

## 🐋 Étape 6 : Docker (optionnel)

### Avec Docker Compose (RECOMMANDÉ) :

```powershell
# Démarrer
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

### Sans Docker Compose :

```powershell
# Construire l'image
docker build -t banking-api:latest .

# Lancer le conteneur
docker run -d -p 8000:8000 `
  -v ${PWD}/data:/app/data `
  --name banking-api `
  banking-api:latest
```

## 📊 Structure des données

Le fichier `transactions_data.csv` doit contenir :
- **~6,3 millions de lignes**
- **Taille** : ~470 MB
- **Colonnes** : step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest, isFraud, isFlaggedFraud

## ⚠️ Dépannage

### Problème : "données non trouvées"
```powershell
# Vérifier le chemin
$env:DATA_PATH = "data\transactions_data.csv"
uvicorn banking_api.main:app --reload
```

### Problème : "module not found"
```powershell
# Réinstaller
pip install -e . --force-reinstall
```

### Problème : Script ne s'exécute pas
```powershell
# Autoriser l'exécution de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📝 Endpoints disponibles (20 routes)

| Catégorie | Nombre | Exemples |
|-----------|--------|----------|
| **Transactions** | 8 | `/api/transactions`, `/api/transactions/{id}` |
| **Statistiques** | 4 | `/api/stats/overview`, `/api/stats/by-type` |
| **Fraude** | 3 | `/api/fraud/summary`, `/api/fraud/predict` |
| **Clients** | 3 | `/api/customers`, `/api/customers/{id}` |
| **Système** | 2 | `/api/system/health`, `/api/system/metadata` |

## 🎓 Conformité au projet

✅ 20 routes FastAPI fonctionnelles  
✅ Conformité PEP8 (flake8)  
✅ Typing complet (mypy)  
✅ Package Python avec setuptools  
✅ Tests pytest (couverture >85%)  
✅ Tests unittest (features)  
✅ Documentation NumPy style  
✅ Docker + docker-compose (BONUS)  
✅ CI/CD GitHub Actions (BONUS)  

## 🆘 Besoin d'aide ?

Consultez :
- `README.md` : Documentation complète
- `DOWNLOAD_DATA.md` : Guide de téléchargement des données
- http://localhost:8000/docs : Documentation API interactive
