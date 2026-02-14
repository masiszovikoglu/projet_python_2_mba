# Script d'installation et de démarrage - Banking API
# Usage: .\setup_and_run.ps1

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Banking Transactions API - Setup & Run" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Étape 1 : Vérifier Python
Write-Host "[1/6] Vérification de Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR: Python n'est pas installé ou n'est pas dans le PATH" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Python détecté: $pythonVersion" -ForegroundColor Green

# Étape 2 : Créer l'environnement virtuel
Write-Host ""
Write-Host "[2/6] Création de l'environnement virtuel..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ L'environnement virtuel existe déjà" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "✓ Environnement virtuel créé" -ForegroundColor Green
}

# Étape 3 : Activer l'environnement virtuel
Write-Host ""
Write-Host "[3/6] Activation de l'environnement virtuel..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Environnement virtuel activé" -ForegroundColor Green

# Étape 4 : Installer les dépendances
Write-Host ""
Write-Host "[4/6] Installation des dépendances..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
pip install -e . --quiet
pip install -e ".[dev]" --quiet
Write-Host "✓ Dépendances installées" -ForegroundColor Green

# Étape 5 : Vérifier les données
Write-Host ""
Write-Host "[5/6] Vérification des données..." -ForegroundColor Yellow
$dataFile = "data\transactions_data.csv"
if (Test-Path $dataFile) {
    $fileSize = (Get-Item $dataFile).Length / 1MB
    Write-Host "✓ Fichier de données trouvé: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Green
} else {
    Write-Host "⚠ Fichier de données non trouvé: $dataFile" -ForegroundColor Yellow
    Write-Host "  Utilisation des données d'exemple pour les tests" -ForegroundColor Yellow
    $env:DATA_PATH = "data\sample_transactions.csv"
}

# Étape 6 : Démarrer l'API
Write-Host ""
Write-Host "[6/6] Démarrage de l'API..." -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  L'API est prête à démarrer!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Documentation Swagger: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Documentation ReDoc:   http://localhost:8000/redoc" -ForegroundColor Cyan
Write-Host "API Root:              http://localhost:8000/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Yellow
Write-Host ""

# Démarrer uvicorn
uvicorn banking_api.main:app --reload --host 0.0.0.0 --port 8000
