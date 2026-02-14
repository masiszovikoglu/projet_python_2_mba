# Script de construction du package - Banking API
# Usage: .\build_package.ps1

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Banking Transactions API - Build Package" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Activer l'environnement virtuel
Write-Host "[1/5] Activation de l'environnement virtuel..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Environnement virtuel activé" -ForegroundColor Green

# Nettoyer les anciens builds
Write-Host ""
Write-Host "[2/5] Nettoyage des anciens builds..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item -Recurse -Force dist }
if (Test-Path "build") { Remove-Item -Recurse -Force build }
if (Test-Path "src\banking_api.egg-info") { Remove-Item -Recurse -Force src\banking_api.egg-info }
Write-Host "✓ Répertoires nettoyés" -ForegroundColor Green

# Installer les outils de build
Write-Host ""
Write-Host "[3/5] Installation des outils de build..." -ForegroundColor Yellow
pip install --upgrade build setuptools wheel --quiet
Write-Host "✓ Outils de build installés" -ForegroundColor Green

# Build avec setuptools
Write-Host ""
Write-Host "[4/5] Build avec setuptools..." -ForegroundColor Yellow
python setup.py sdist bdist_wheel
Write-Host "✓ Build setuptools terminé" -ForegroundColor Green

# Build avec python -m build
Write-Host ""
Write-Host "[5/5] Build avec module build..." -ForegroundColor Yellow
python -m build
Write-Host "✓ Build module build terminé" -ForegroundColor Green

# Afficher les résultats
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  Build terminé avec succès!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Fichiers générés dans dist/:" -ForegroundColor Cyan
Get-ChildItem dist\ | ForEach-Object {
    $size = [math]::Round($_.Length / 1KB, 2)
    Write-Host "  → $($_.Name) ($size KB)" -ForegroundColor White
}

Write-Host ""
Write-Host "Installation du package:" -ForegroundColor Yellow
Write-Host "  pip install dist/banking_transactions_api-1.0.0-py3-none-any.whl" -ForegroundColor White
