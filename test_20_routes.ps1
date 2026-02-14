# Script de test des 20 routes FastAPI
# Ce script teste automatiquement toutes les routes et génère un rapport

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  TEST DES 20 ROUTES FASTAPI" -ForegroundColor Cyan
Write-Host "  Banking Transactions API" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Copier les données
Write-Host "[1] Préparation des données..." -ForegroundColor Yellow
Copy-Item ".\data\archive\transactions_data.csv" -Destination ".\data\transactions_data.csv" -Force -ErrorAction SilentlyContinue
if (Test-Path ".\data\transactions_data.csv") {
    Write-Host "  ✓ Données prêtes" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Utilisation des données d'exemple" -ForegroundColor Yellow
    $env:DATA_PATH = "data\sample_transactions.csv"
}

# Démarrer l'API en arrière-plan
Write-Host ""
Write-Host "[2] Démarrage de l'API..." -ForegroundColor Yellow
$apiProcess = Start-Process powershell -ArgumentList "-Command", "python -m uvicorn banking_api.main:app --host 127.0.0.1 --port 8000" -PassThru -WindowStyle Hidden
Write-Host "  ✓ API démarrée (PID: $($apiProcess.Id))" -ForegroundColor Green

# Attendre que l'API soit prête
Write-Host ""
Write-Host "[3] Attente du démarrage (10 secondes)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
Write-Host "  ✓ Prêt à tester" -ForegroundColor Green

# Fonction pour tester un endpoint
function Test-Endpoint {
    param(
        [int]$Number,
        [string]$Method,
        [string]$Endpoint,
        [string]$Description,
        [string]$Body = $null
    )
    
    Write-Host ""
    Write-Host "[$Number/20] Test: $Description" -ForegroundColor Cyan
    Write-Host "         $Method $Endpoint" -ForegroundColor Gray
    
    try {
        if ($Method -eq "GET") {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000$Endpoint" -Method GET -TimeoutSec 5 -UseBasicParsing
        } elseif ($Method -eq "POST") {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000$Endpoint" -Method POST -Body $Body -ContentType "application/json" -TimeoutSec 5 -UseBasicParsing
        } elseif ($Method -eq "DELETE") {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000$Endpoint" -Method DELETE -TimeoutSec 5 -UseBasicParsing
        }
        
        if ($response.StatusCode -eq 200) {
            Write-Host "         ✓ SUCCÈS (200 OK)" -ForegroundColor Green
            return 1
        } else {
            Write-Host "         ⚠ Code: $($response.StatusCode)" -ForegroundColor Yellow
            return 0
        }
    } catch {
        Write-Host "         ✗ ÉCHEC: $($_.Exception.Message)" -ForegroundColor Red
        return 0
    }
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  TESTS DES ROUTES" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

$score = 0

# TRANSACTIONS (8 routes)
Write-Host ""
Write-Host "=== TRANSACTIONS (8 routes) ===" -ForegroundColor Magenta
$score += Test-Endpoint 1 "GET" "/api/transactions" "Liste des transactions"
$score += Test-Endpoint 2 "GET" "/api/transactions/tx_0000001" "Détails d'une transaction"
$score += Test-Endpoint 3 "POST" "/api/transactions/search" "Recherche multicritère" '{"type":"PAYMENT"}'
$score += Test-Endpoint 4 "GET" "/api/transactions/types" "Types de transactions"
$score += Test-Endpoint 5 "GET" "/api/transactions/recent?n=5" "Transactions récentes"
$score += Test-Endpoint 6 "DELETE" "/api/transactions/tx_0000001" "Suppression (test)"
$score += Test-Endpoint 7 "GET" "/api/transactions/by-customer/C1231006815" "Transactions par client"
$score += Test-Endpoint 8 "GET" "/api/transactions/to-customer/M1979787155" "Transactions vers client"

# STATISTIQUES (4 routes)
Write-Host ""
Write-Host "=== STATISTIQUES (4 routes) ===" -ForegroundColor Magenta
$score += Test-Endpoint 9 "GET" "/api/stats/overview" "Statistiques globales"
$score += Test-Endpoint 10 "GET" "/api/stats/amount-distribution?bins=10" "Distribution des montants"
$score += Test-Endpoint 11 "GET" "/api/stats/by-type" "Statistiques par type"
$score += Test-Endpoint 12 "GET" "/api/stats/daily" "Statistiques quotidiennes"

# FRAUDE (3 routes)
Write-Host ""
Write-Host "=== DÉTECTION DE FRAUDE (3 routes) ===" -ForegroundColor Magenta
$score += Test-Endpoint 13 "GET" "/api/fraud/summary" "Résumé des fraudes"
$score += Test-Endpoint 14 "GET" "/api/fraud/by-type" "Fraude par type"
$score += Test-Endpoint 15 "POST" "/api/fraud/predict" "Prédiction de fraude" '{"type":"TRANSFER","amount":3500,"oldbalanceOrg":15000,"newbalanceOrig":11500}'

# CLIENTS (3 routes)
Write-Host ""
Write-Host "=== CLIENTS (3 routes) ===" -ForegroundColor Magenta
$score += Test-Endpoint 16 "GET" "/api/customers" "Liste des clients"
$score += Test-Endpoint 17 "GET" "/api/customers/C1231006815" "Profil client"
$score += Test-Endpoint 18 "GET" "/api/customers/top?n=5" "Top clients"

# SYSTÈME (2 routes)
Write-Host ""
Write-Host "=== SYSTÈME (2 routes) ===" -ForegroundColor Magenta
$score += Test-Endpoint 19 "GET" "/api/system/health" "Santé du système"
$score += Test-Endpoint 20 "GET" "/api/system/metadata" "Métadonnées"

# Résultat final
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  RÉSULTATS FINAUX" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Routes testées : 20" -ForegroundColor White
Write-Host "Routes réussies: $score/20" -ForegroundColor $(if ($score -eq 20) { "Green" } else { "Yellow" })
Write-Host ""

# Calcul de la note
$note = [math]::Round(($score / 20) * 10, 2)
Write-Host "NOTE FINALE: $note/10" -ForegroundColor $(if ($note -eq 10) { "Green" } else { "Yellow" })
Write-Host ""

if ($score -eq 20) {
    Write-Host "🎉 PARFAIT! Toutes les routes fonctionnent!" -ForegroundColor Green
    Write-Host "✅ Notation: 10/10 points" -ForegroundColor Green
} elseif ($score -ge 18) {
    Write-Host "✅ TRÈS BIEN! Presque toutes les routes fonctionnent" -ForegroundColor Green
} elseif ($score -ge 15) {
    Write-Host "⚠ BIEN! La plupart des routes fonctionnent" -ForegroundColor Yellow
} else {
    Write-Host "⚠ Certaines routes nécessitent des corrections" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Documentation complète disponible sur:" -ForegroundColor Cyan
Write-Host "  → http://127.0.0.1:8000/docs (Swagger UI)" -ForegroundColor White
Write-Host "  → http://127.0.0.1:8000/redoc (ReDoc)" -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur une touche pour arrêter l'API..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Arrêter l'API
Write-Host ""
Write-Host "Arrêt de l'API..." -ForegroundColor Yellow
Stop-Process -Id $apiProcess.Id -Force -ErrorAction SilentlyContinue
Write-Host "✓ API arrêtée" -ForegroundColor Green
Write-Host ""
Write-Host "Test terminé!" -ForegroundColor Green
