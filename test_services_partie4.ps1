# ═══════════════════════════════════════════════════════════════
# TEST DES 5 SERVICES INTERNES - PARTIE 4 ESG MBA
# ═══════════════════════════════════════════════════════════════

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "🔧 VALIDATION DES 5 SERVICES INTERNES - PARTIE 4 ESG MBA" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════`n" -ForegroundColor Yellow

$baseUrl = "http://127.0.0.1:8000"
$results = @()
$successCount = 0

function Test-Service {
    param(
        [int]$Number,
        [string]$ServiceName,
        [string]$Role,
        [string]$TestUrl,
        [string]$Method = "GET",
        [object]$Body = $null
    )
    
    Write-Host "[$Number/5] 📦 $ServiceName" -ForegroundColor Cyan
    Write-Host "  🎯 Rôle: $Role" -ForegroundColor Gray
    Write-Host "  🧪 Test: $Method $TestUrl" -ForegroundColor DarkGray
    
    try {
        $params = @{
            Uri = $TestUrl
            Method = $Method
            TimeoutSec = 30
            ErrorAction = "Stop"
        }
        
        if ($Body) {
            $params.Body = ($Body | ConvertTo-Json)
            $params.ContentType = "application/json"
        }
        
        $response = Invoke-RestMethod @params
        
        Write-Host "  ✅ Service fonctionnel!" -ForegroundColor Green
        
        # Afficher aperçu de la réponse
        if ($response -is [array] -and $response.Count -gt 0) {
            Write-Host "  📊 Résultat: $($response.Count) éléments retournés" -ForegroundColor DarkGreen
        } elseif ($response.PSObject.Properties.Count -gt 0) {
            $keys = ($response.PSObject.Properties.Name | Select-Object -First 5) -join ", "
            Write-Host "  📊 Propriétés: $keys..." -ForegroundColor DarkGreen
        }
        
        $script:successCount++
        $script:results += [PSCustomObject]@{
            "#" = $Number
            Service = $ServiceName
            Status = "✅ OK"
            Test = "Passé"
        }
        Write-Host ""
        
    } catch {
        Write-Host "  ❌ ERREUR: $($_.Exception.Message)" -ForegroundColor Red
        $script:results += [PSCustomObject]@{
            "#" = $Number
            Service = $ServiceName
            Status = "❌ ERREUR"
            Test = "Échoué"
        }
        Write-Host ""
    }
}

# ═══════════════════════════════════════════════════════════════
# TEST 1: transactions_service.py
# ═══════════════════════════════════════════════════════════════
Test-Service `
    -Number 1 `
    -ServiceName "transactions_service.py" `
    -Role "Lecture, pagination, filtrage, recherche multi-critères" `
    -TestUrl "$baseUrl/api/transactions?skip=0&limit=5" `
    -Method "GET"

# ═══════════════════════════════════════════════════════════════
# TEST 2: stats_service.py
# ═══════════════════════════════════════════════════════════════
Test-Service `
    -Number 2 `
    -ServiceName "stats_service.py" `
    -Role "Calcul des agrégations et distributions" `
    -TestUrl "$baseUrl/api/stats/overview" `
    -Method "GET"

# ═══════════════════════════════════════════════════════════════
# TEST 3: fraud_detection_service.py
# ═══════════════════════════════════════════════════════════════
$fraudBody = @{
    amount = 5000.0
    use_chip = "Online Transaction"
    mcc = 5816
    merchant_state = "FL"
}
Test-Service `
    -Number 3 `
    -ServiceName "fraud_detection_service.py" `
    -Role "Calcul de taux de fraude, scoring simplifié" `
    -TestUrl "$baseUrl/api/fraud/predict" `
    -Method "POST" `
    -Body $fraudBody

# ═══════════════════════════════════════════════════════════════
# TEST 4: customer_service.py
# ═══════════════════════════════════════════════════════════════
Test-Service `
    -Number 4 `
    -ServiceName "customer_service.py" `
    -Role "Agrégation par client" `
    -TestUrl "$baseUrl/api/customers/1556" `
    -Method "GET"

# ═══════════════════════════════════════════════════════════════
# TEST 5: system_service.py
# ═══════════════════════════════════════════════════════════════
Test-Service `
    -Number 5 `
    -ServiceName "system_service.py" `
    -Role "Diagnostic du service et métadonnées" `
    -TestUrl "$baseUrl/api/system/health" `
    -Method "GET"

# ═══════════════════════════════════════════════════════════════
# RÉSUMÉ FINAL
# ═══════════════════════════════════════════════════════════════

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "📊 RÉSULTATS - SERVICES INTERNES (PARTIE 4)" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════`n" -ForegroundColor Yellow

$results | Format-Table -AutoSize

Write-Host "`n📈 STATISTIQUES:" -ForegroundColor Cyan
Write-Host "  ✅ Services fonctionnels: $successCount / 5" -ForegroundColor $(if ($successCount -eq 5) { "Green" } else { "Red" })
Write-Host "  ❌ Services en erreur: $(5 - $successCount) / 5" -ForegroundColor $(if ($successCount -eq 5) { "Green" } else { "Red" })

if ($successCount -eq 5) {
    Write-Host "`n🎉 PARFAIT! TOUS LES 5 SERVICES INTERNES FONCTIONNENT!" -ForegroundColor Green
    Write-Host "✅ Conformité totale à la Partie 4 des spécifications ESG MBA" -ForegroundColor Green
    Write-Host "`n📋 Services validés:" -ForegroundColor Cyan
    Write-Host "  1. ✅ transactions_service.py - Lecture, pagination, filtrage" -ForegroundColor Green
    Write-Host "  2. ✅ stats_service.py - Agrégations et distributions" -ForegroundColor Green
    Write-Host "  3. ✅ fraud_detection_service.py - Scoring de fraude" -ForegroundColor Green
    Write-Host "  4. ✅ customer_service.py - Agrégation clients" -ForegroundColor Green
    Write-Host "  5. ✅ system_service.py - Diagnostic système" -ForegroundColor Green
} else {
    Write-Host "`n⚠️ $(5 - $successCount) service(s) nécessite(nt) correction" -ForegroundColor Yellow
}

Write-Host "`n═══════════════════════════════════════════════════════════════`n" -ForegroundColor Yellow

# Vérification des fichiers
Write-Host "📁 VÉRIFICATION DES FICHIERS:" -ForegroundColor Cyan
$serviceFiles = @(
    "src\banking_api\services\transactions_service.py",
    "src\banking_api\services\stats_service.py",
    "src\banking_api\services\fraud_detection_service.py",
    "src\banking_api\services\customer_service.py",
    "src\banking_api\services\system_service.py"
)

$filesPresent = 0
foreach ($file in $serviceFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
        $filesPresent++
    } else {
        Write-Host "  ❌ $file (manquant)" -ForegroundColor Red
    }
}

Write-Host "`n📊 Fichiers présents: $filesPresent / 5" -ForegroundColor Cyan

if ($successCount -eq 5 -and $filesPresent -eq 5) {
    Write-Host "`n🏆 VALIDATION COMPLÈTE PARTIE 4: 100% CONFORME" -ForegroundColor Green
    exit 0
} else {
    exit 1
}
