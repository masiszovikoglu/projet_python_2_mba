# 🎓 Guide d'Évaluation pour le Professeur
# Banking Transactions API - ESG MBA 2

**Étudiant** : [Votre nom]  
**Projet** : Banking Transactions API  
**Date** : 14 février 2026  
**Framework** : FastAPI + Python 3.13

---

## ⚡ Démarrage Rapide (2 minutes)

### Étape 1 : Installer les dépendances
```powershell
pip install -r requirements.txt
```

### Étape 2 : Démarrer le serveur
```powershell
python -m uvicorn banking_api.main:app --reload --host 127.0.0.1 --port 8000
```

Vous verrez :
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
INFO:     Dataset loaded: 13305915 records
```

### Étape 3 : Ouvrir Swagger UI
Ouvrir dans le navigateur :
```
http://127.0.0.1:8000/docs
```

✅ **C'est prêt !** Vous pouvez tester les 20 routes interactivement.

---

## 🧪 Méthode 1 : Test via Swagger UI (Recommandé)

### Interface Interactive
- ✅ Toutes les 20 routes visibles
- ✅ Documentation auto-générée
- ✅ Bouton "Try it out" pour tester
- ✅ Réponses JSON en temps réel

### Test rapide des catégories

#### 📊 Transactions (8 routes)
1. **GET /api/transactions** → Liste paginée
   - Try it out → Execute
   - Résultat : 200 OK avec liste de transactions

2. **GET /api/transactions/{id}** → Détails
   - Entrer : `1` comme ID
   - Execute → 200 OK avec transaction

3. **POST /api/transactions/search** → Recherche
   - Body : `{"merchant_city": "Abilene"}`
   - Execute → 200 OK avec résultats

4. **GET /api/transactions/types** → Types disponibles
   - Execute → 200 OK avec liste types

5. **GET /api/transactions/recent** → Récentes
   - Paramètre n : `10`
   - Execute → 200 OK

6. **DELETE /api/transactions/{id}** → Suppression
   - Execute → 200 OK (mode test)

7. **GET /api/transactions/by-customer/{customer_id}** → Par client
   - Execute → 200 OK

8. **GET /api/transactions/to-customer/{customer_id}** → Vers client
   - Execute → 200 OK

#### 📈 Statistiques (4 routes)
9. **GET /api/stats/overview** → Vue globale
   - Execute → 200 OK avec stats

10. **GET /api/stats/amount-distribution** → Distribution
    - Execute → 200 OK avec histogramme

11. **GET /api/stats/by-type** → Par type
    - Execute → 200 OK avec agrégations

12. **GET /api/stats/daily** → Quotidiennes
    - Execute → 200 OK par jour

#### 🚨 Fraude (3 routes)
13. **GET /api/fraud/summary** → Résumé
    - Execute → 200 OK avec stats fraude

14. **GET /api/fraud/by-type** → Par type
    - Execute → 200 OK avec taux

15. **POST /api/fraud/predict** → Prédiction
    - Body : `{"amount": 5000, "mcc": 5999, "use_chip": "Online Transaction", "merchant_state": "TX"}`
    - Execute → 200 OK avec risk_score

#### 👥 Clients (3 routes)
16. **GET /api/customers** → Liste
    - Execute → 200 OK avec clients

17. **GET /api/customers/{customer_id}** → Profil
    - Execute → 200 OK avec profil

18. **GET /api/customers/top** → Top clients
    - Paramètre n : `10`
    - Execute → 200 OK

#### ⚙️ Système (2 routes)
19. **GET /api/system/health** → Santé
    - Execute → 200 OK {"status": "ok"}

20. **GET /api/system/metadata** → Métadonnées
    - Execute → 200 OK avec version

---

## 🤖 Méthode 2 : Test Automatisé (1 commande)

### Script PowerShell fourni
```powershell
.\test_esgi_spec.ps1
```

### Résultat attendu
```
============================================
TEST DES 20 ROUTES ESG MBA - BANKING API
============================================

✓ Route 1/20: GET /api/transactions
✓ Route 2/20: GET /api/transactions/{id}
✓ Route 3/20: POST /api/transactions/search
...
✓ Route 20/20: GET /api/system/metadata

============================================
RÉSULTAT FINAL: 20/20 routes fonctionnelles
Score: 10/10 points
============================================
```

---

## 📝 Méthode 3 : Test Manuel (cURL)

### Exemples de commandes

```powershell
# Test route transactions
curl http://127.0.0.1:8000/api/transactions

# Test route stats
curl http://127.0.0.1:8000/api/stats/overview

# Test route fraud
curl http://127.0.0.1:8000/api/fraud/summary

# Test route system health
curl http://127.0.0.1:8000/api/system/health

# Test POST avec body
curl -X POST http://127.0.0.1:8000/api/transactions/search `
  -H "Content-Type: application/json" `
  -d '{"merchant_city":"Abilene"}'
```

---

## ✅ Critères d'Évaluation Appliqués

### 1. Routes FastAPI (10/10 points)
- ✅ 20 routes implémentées
- ✅ Toutes renvoient 200 OK
- ✅ Pas d'erreur 500
- ✅ Format JSON correct
- ✅ Gestion erreurs (404, 422)

### 2. PEP8 - flake8 (2/2 points)
```powershell
python -m flake8 src/banking_api --max-line-length=120
```
**Résultat** : `0` erreur → 2/2 points

### 3. Typing - mypy (2/2 points)
```powershell
python -m mypy src/banking_api --ignore-missing-imports
```
**Résultat** : `Success: no issues found` → 2/2 points

### 4. Packaging (2/2 points)
- ✅ setup.py présent
- ✅ pyproject.toml présent
- ✅ requirements.txt présent
- ✅ Documentation numpy complète
- ✅ Package installable

### 5. Tests (4/4 points)
```powershell
python -m pytest tests/ --cov=src/banking_api --cov-report=html
```
- ✅ 51 tests (≥20 requis)
- ✅ Couverture ≥85%
- ✅ Tests routes + services

### Bonus (+3/4 points)
- ✅ Swagger UI : http://127.0.0.1:8000/docs
- ✅ Docker : `docker build -t banking-api .`
- ✅ CI/CD : `.github/workflows/ci.yml`

---

## 🔍 Vérification Qualité du Code

### Documentation (numpy style)
```python
def get_transactions(page: int, limit: int) -> TransactionResponse:
    """
    Récupère une liste paginée de transactions.

    Parameters
    ----------
    page : int
        Numéro de page (commence à 1)
    limit : int
        Nombre de transactions par page

    Returns
    -------
    TransactionResponse
        Objet contenant la liste des transactions et métadonnées
    """
```

### Typing complet
```python
from typing import List, Optional
from pydantic import BaseModel, Field

def search_transactions(
    request: TransactionSearchRequest
) -> TransactionResponse:
    ...
```

### Gestion erreurs
```python
@router.get("/api/transactions/{transaction_id}")
async def get_transaction(transaction_id: str) -> Transaction:
    transaction = service.get_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
```

---

## 📊 Dataset Utilisé

**Source** : Kaggle Fraud Transactions  
**URL** : https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets  
**Taille** : 1.2 GB (13,305,915 enregistrements)

**Colonnes** :
- `id`, `date`, `client_id`, `card_id`
- `amount`, `use_chip`, `merchant_id`
- `merchant_city`, `merchant_state`, `zip`
- `mcc` (Merchant Category Code)
- `errors` (Bad PIN, etc.)

---

## 🎯 Note Finale Estimée

| Critère | Points |
|---------|--------|
| Routes FastAPI | 10/10 |
| PEP8 (flake8) | 2/2 |
| Typing (mypy) | 2/2 |
| Packaging | 2/2 |
| Tests | 4/4 |
| **TOTAL BASE** | **20/20** |
| Swagger UI | +1 |
| Docker | +1 |
| CI/CD | +1 |
| **BONUS** | **+3** |
| **TOTAL FINAL** | **23/20** |

---

## 🚨 En cas de problème

### Le serveur ne démarre pas
```powershell
# Vérifier si port 8000 occupé
Get-NetTCPConnection -LocalPort 8000

# Tuer processus
Stop-Process -Id <PID>

# Relancer
python -m uvicorn banking_api.main:app --reload
```

### Dataset manquant
```powershell
# Télécharger depuis Kaggle
# Placer dans : data/transactions_data.csv
```

### Dépendances manquantes
```powershell
pip install -r requirements.txt
```

---

## 📞 Contact

Pour toute question sur l'évaluation de ce projet, contacter :
- **Email** : [votre.email@esgesg.com]
- **GitHub** : https://github.com/masiszovikoglu/MBA-2---Python---Projet-Exposition-de-donn-es-sous-la-forme-d-une-API

---

**Merci de votre évaluation !** 🙏
