# Script de test rapide - Banking API
# Usage: .\quick_test.ps1

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Banking Transactions API - Quick Test" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Activer l'environnement virtuel
Write-Host "[1/4] Activation de l'environnement virtuel..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Environnement virtuel activé" -ForegroundColor Green

# Lancer les tests pytest
Write-Host ""
Write-Host "[2/4] Exécution des tests pytest..." -ForegroundColor Yellow
pytest tests/ -v --cov=src/banking_api --cov-report=term-missing

# Lancer les tests unittest
Write-Host ""
Write-Host "[3/4] Exécution des tests unittest..." -ForegroundColor Yellow
python -m unittest discover -s tests -p "test_features.py" -v

# Vérifier la qualité du code
Write-Host ""
Write-Host "[4/4] Vérification de la qualité du code..." -ForegroundColor Yellow
Write-Host "  → Flake8..." -ForegroundColor Cyan
flake8 src/banking_api/ --count --statistics

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  Tests terminés!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
