# Test complet des 20 routes FastAPI
# MBA-2 Project - Banking Transactions API

$baseUrl = "http://127.0.0.1:8000"
$results = @()
$successCount = 0
$failureCount = 0

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Method,
        [string]$Url,
        [object]$Body = $null
    )
    
    Write-Host "`n[$($results.Count + 1)/20] $Name" -ForegroundColor Cyan
    Write-Host "  → $Method $Url" -ForegroundColor Gray
    
    try {
        $params = @{
            Uri = $Url
            Method = $Method
            TimeoutSec = 30
            ErrorAction = "Stop"
        }
        
        if ($Body) {
            $params.Body = ($Body | ConvertTo-Json)
            $params.ContentType = "application/json"
        }
        
        $response = Invoke-RestMethod @params
        
        Write-Host "  ✅ SUCCESS (200 OK)" -ForegroundColor Green
        $script:successCount++
        $script:results += [PSCustomObject]@{
            Route = $Name
            Status = "✅ OK"
            Method = $Method
        }
        
        # Afficher un aperçu de la réponse
        if ($response -is [array] -and $response.Count -gt 0) {
            Write-Host "  📊 Résultat: $($response.Count) éléments" -ForegroundColor Gray
        } elseif ($response.PSObject.Properties.Count -gt 0) {
            $preview = ($response | ConvertTo-Json -Depth 1 -Compress).Substring(0, [Math]::Min(100, ($response | ConvertTo-Json -Depth 1 -Compress).Length))
            Write-Host "  📊 Aperçu: $preview..." -ForegroundColor Gray
        }
        
    } catch {
        Write-Host "  ❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
        $script:failureCount++
        $script:results += [PSCustomObject]@{
            Route = $Name
            Status = "❌ ERREUR"
            Method = $Method
        }
    }
}

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "🧪 TEST COMPLET DES 20 ROUTES - MBA-2 Banking API" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════`n" -ForegroundColor Yellow

# ==================== SYSTEM ROUTES (2) ====================
Write-Host "📦 SYSTEM ROUTES (2)" -ForegroundColor Magenta
Test-Endpoint "Health Check" "GET" "$baseUrl/api/system/health"
Test-Endpoint "Metadata" "GET" "$baseUrl/api/system/metadata"

# ==================== TRANSACTIONS ROUTES (8) ====================
Write-Host "`n📦 TRANSACTIONS ROUTES (8)" -ForegroundColor Magenta
Test-Endpoint "Liste transactions" "GET" "$baseUrl/api/transactions?skip=0&limit=10"
Test-Endpoint "Transaction par ID" "GET" "$baseUrl/api/transactions/7475327"
Test-Endpoint "Types de transactions" "GET" "$baseUrl/api/transactions/types"
Test-Endpoint "Transactions récentes" "GET" "$baseUrl/api/transactions/recent?limit=5"
Test-Endpoint "Transactions par client" "GET" "$baseUrl/api/transactions/by-customer?client_id=1556&limit=5"
Test-Endpoint "Transactions vers marchand" "GET" "$baseUrl/api/transactions/to-merchant?merchant_id=59935&limit=5"

$searchBody = @{
    client_id = 1556
    min_amount = -100.0
    max_amount = 0.0
    limit = 5
}
Test-Endpoint "Recherche transactions" "POST" "$baseUrl/api/transactions/search" $searchBody

Test-Endpoint "Suppression transaction" "DELETE" "$baseUrl/api/transactions/9999999999"

# ==================== STATS ROUTES (4) ====================
Write-Host "`n📦 STATS ROUTES (4)" -ForegroundColor Magenta
Test-Endpoint "Aperçu statistiques" "GET" "$baseUrl/api/stats/overview"
Test-Endpoint "Distribution montants" "GET" "$baseUrl/api/stats/amount-distribution?buckets=5"
Test-Endpoint "Stats par type chip" "GET" "$baseUrl/api/stats/by-chip"
Test-Endpoint "Stats quotidiennes" "GET" "$baseUrl/api/stats/daily?limit=7"

# ==================== FRAUD ROUTES (3) ====================
Write-Host "`n📦 FRAUD ROUTES (3)" -ForegroundColor Magenta
Test-Endpoint "Résumé fraude" "GET" "$baseUrl/api/fraud/summary"
Test-Endpoint "Fraude par marchand" "GET" "$baseUrl/api/fraud/by-merchant?limit=10"

$fraudBody = @{
    amount = 5000.0
    use_chip = "Online Transaction"
    mcc = 5816
    merchant_state = "FL"
}
Test-Endpoint "Prédiction fraude" "POST" "$baseUrl/api/fraud/predict" $fraudBody

# ==================== CUSTOMERS ROUTES (3) ====================
Write-Host "`n📦 CUSTOMERS ROUTES (3)" -ForegroundColor Magenta
Test-Endpoint "Liste clients" "GET" "$baseUrl/api/customers?skip=0&limit=10"
Test-Endpoint "Profil client" "GET" "$baseUrl/api/customers/1556"
Test-Endpoint "Top clients" "GET" "$baseUrl/api/customers/top?limit=10"

# ==================== RÉSUMÉ ====================
Write-Host "`n═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "📊 RÉSULTATS FINAUX" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════`n" -ForegroundColor Yellow

$results | Format-Table -AutoSize

Write-Host "`n✅ SUCCÈS: $successCount / 20" -ForegroundColor Green
Write-Host "❌ ÉCHECS: $failureCount / 20" -ForegroundColor Red

if ($successCount -eq 20) {
    Write-Host "`n🎉 PARFAIT! TOUTES LES ROUTES FONCTIONNENT!" -ForegroundColor Green
    Write-Host "🏆 Score attendu: 10/10 pour les routes fonctionnelles" -ForegroundColor Green
} elseif ($successCount -ge 18) {
    Write-Host "`n⚠️ Presque parfait! $successCount/20 routes OK" -ForegroundColor Yellow
} else {
    Write-Host "`n⚠️ $failureCount routes nécessitent correction" -ForegroundColor Yellow
}

Write-Host "`n═══════════════════════════════════════════════════════════════`n" -ForegroundColor Yellow
