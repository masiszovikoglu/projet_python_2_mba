# ═══════════════════════════════════════════════════════════════
# TEST DE CONFORMITÉ - PARTIE 5: TESTS UNITAIRES ESG MBA
# ═══════════════════════════════════════════════════════════════

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "🧪 VALIDATION PARTIE 5 - TESTS UNITAIRES ESG MBA" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════`n" -ForegroundColor Yellow

$results = @()
$totalPoints = 0
$maxPoints = 5

# ═══════════════════════════════════════════════════════════════
# 1. TESTS ROUTES (≥20 tests attendus)
# ═══════════════════════════════════════════════════════════════
Write-Host "[1/5] 📋 Tests sur les routes (1 test par endpoint)" -ForegroundColor Cyan

# Compter les tests
$testFiles = Get-ChildItem -Path "tests\" -Filter "*.py" -Recurse
$totalTests = 0

foreach ($file in $testFiles) {
    $content = Get-Content $file.FullName -Raw
    $testCount = ([regex]::Matches($content, "def test_")).Count
    Write-Host "  📄 $($file.Name): $testCount tests" -ForegroundColor Gray
    $totalTests += $testCount
}

Write-Host "`n  📊 Total tests trouvés: $totalTests" -ForegroundColor White

if ($totalTests -ge 20) {
    Write-Host "  ✅ CONFORME: ≥20 tests (objectif atteint)" -ForegroundColor Green
    $results += [PSCustomObject]@{
        Critère = "Tests Routes"
        Requis = "≥20 tests"
        Obtenu = "$totalTests tests"
        Status = "✅ OK"
    }
    $totalPoints++
} else {
    Write-Host "  ⚠️ ATTENTION: $totalTests tests (20 requis)" -ForegroundColor Yellow
    $results += [PSCustomObject]@{
        Critère = "Tests Routes"
        Requis = "≥20 tests"
        Obtenu = "$totalTests tests"
        Status = "⚠️ Partiel"
    }
}
Write-Host ""

# ═══════════════════════════════════════════════════════════════
# 2. TESTS SERVICES (stats et fraude)
# ═══════════════════════════════════════════════════════════════
Write-Host "[2/5] 🔧 Tests sur les services (stats et fraude)" -ForegroundColor Cyan

$statsTests = 0
$fraudTests = 0

if (Test-Path "tests\test_stats_service.py") {
    $content = Get-Content "tests\test_stats_service.py" -Raw
    $statsTests = ([regex]::Matches($content, "def test_")).Count
    Write-Host "  📄 test_stats_service.py: $statsTests tests" -ForegroundColor Gray
}

if (Test-Path "tests\test_fraud_service.py") {
    $content = Get-Content "tests\test_fraud_service.py" -Raw
    $fraudTests = ([regex]::Matches($content, "def test_")).Count
    Write-Host "  📄 test_fraud_service.py: $fraudTests tests" -ForegroundColor Gray
}

$serviceTests = $statsTests + $fraudTests
Write-Host "`n  📊 Tests services: $serviceTests" -ForegroundColor White

if ($serviceTests -ge 5) {
    Write-Host "  ✅ CONFORME: Tests stats et fraude présents" -ForegroundColor Green
    $results += [PSCustomObject]@{
        Critère = "Tests Services"
        Requis = "Stats + Fraude"
        Obtenu = "$statsTests stats, $fraudTests fraude"
        Status = "✅ OK"
    }
    $totalPoints++
} else {
    Write-Host "  ⚠️ ATTENTION: Tests services insuffisants" -ForegroundColor Yellow
    $results += [PSCustomObject]@{
        Critère = "Tests Services"
        Requis = "Stats + Fraude"
        Obtenu = "$statsTests stats, $fraudTests fraude"
        Status = "⚠️ Partiel"
    }
}
Write-Host ""

# ═══════════════════════════════════════════════════════════════
# 3. VALIDATIONS JSON
# ═══════════════════════════════════════════════════════════════
Write-Host "[3/5] 📝 Validations format JSON (Pydantic)" -ForegroundColor Cyan

# Vérifier utilisation Pydantic
$modelsFile = "src\banking_api\models.py"
if (Test-Path $modelsFile) {
    $content = Get-Content $modelsFile -Raw
    $pydanticModels = ([regex]::Matches($content, "class \w+\(BaseModel\)")).Count
    Write-Host "  📊 Modèles Pydantic trouvés: $pydanticModels" -ForegroundColor Gray
    
    if ($pydanticModels -ge 10) {
        Write-Host "  ✅ CONFORME: Validation Pydantic implémentée" -ForegroundColor Green
        $results += [PSCustomObject]@{
            Critère = "Validations JSON"
            Requis = "Format entrées"
            Obtenu = "$pydanticModels modèles Pydantic"
            Status = "✅ OK"
        }
        $totalPoints++
    } else {
        Write-Host "  ⚠️ Validations limitées" -ForegroundColor Yellow
        $results += [PSCustomObject]@{
            Critère = "Validations JSON"
            Requis = "Format entrées"
            Obtenu = "$pydanticModels modèles"
            Status = "⚠️ Partiel"
        }
    }
} else {
    Write-Host "  ❌ Fichier models.py non trouvé" -ForegroundColor Red
    $results += [PSCustomObject]@{
        Critère = "Validations JSON"
        Requis = "Format entrées"
        Obtenu = "Non trouvé"
        Status = "❌ Manquant"
    }
}
Write-Host ""

# ═══════════════════════════════════════════════════════════════
# 4. PERFORMANCE (< 500ms pour 100 transactions)
# ═══════════════════════════════════════════════════════════════
Write-Host "[4/5] ⚡ Performance (latence < 500ms pour 100 transactions)" -ForegroundColor Cyan

$baseUrl = "http://127.0.0.1:8000"
Write-Host "  🧪 Test: GET /api/transactions?limit=100" -ForegroundColor Gray

try {
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    $response = Invoke-RestMethod -Uri "$baseUrl/api/transactions?skip=0&limit=100" -Method GET -ErrorAction Stop
    $stopwatch.Stop()
    $latency = $stopwatch.ElapsedMilliseconds
    
    Write-Host "  ⏱️  Latence mesurée: ${latency}ms" -ForegroundColor White
    
    if ($latency -lt 500) {
        Write-Host "  ✅ CONFORME: Latence < 500ms" -ForegroundColor Green
        $results += [PSCustomObject]@{
            Critère = "Performance"
            Requis = "< 500ms"
            Obtenu = "${latency}ms"
            Status = "✅ OK"
        }
        $totalPoints++
    } else {
        Write-Host "  ⚠️ Latence élevée (> 500ms)" -ForegroundColor Yellow
        $results += [PSCustomObject]@{
            Critère = "Performance"
            Requis = "< 500ms"
            Obtenu = "${latency}ms"
            Status = "⚠️ Lent"
        }
    }
} catch {
    Write-Host "  ❌ Test échoué: $($_.Exception.Message)" -ForegroundColor Red
    $results += [PSCustomObject]@{
        Critère = "Performance"
        Requis = "< 500ms"
        Obtenu = "Erreur test"
        Status = "❌ Échec"
    }
}
Write-Host ""

# ═══════════════════════════════════════════════════════════════
# 5. COUVERTURE (≥85%)
# ═══════════════════════════════════════════════════════════════
Write-Host "[5/5] 📊 Couverture de code (cible ≥85%)" -ForegroundColor Cyan

# Exécuter pytest avec coverage
Write-Host "  🧪 Exécution: pytest --cov..." -ForegroundColor Gray
try {
    $coverageOutput = pytest tests/ --cov=src/banking_api --cov-report=term-missing --quiet 2>&1 | Out-String
    
    # Extraire le pourcentage de couverture
    if ($coverageOutput -match "TOTAL\s+\d+\s+\d+\s+(\d+)%") {
        $coverage = [int]$matches[1]
        Write-Host "  📊 Couverture mesurée: $coverage%" -ForegroundColor White
        
        if ($coverage -ge 85) {
            Write-Host "  ✅ CONFORME: Couverture ≥85%" -ForegroundColor Green
            $results += [PSCustomObject]@{
                Critère = "Couverture"
                Requis = "≥85%"
                Obtenu = "$coverage%"
                Status = "✅ OK"
            }
            $totalPoints++
        } elseif ($coverage -ge 70) {
            Write-Host "  ⚠️ Couverture acceptable mais < 85%" -ForegroundColor Yellow
            $results += [PSCustomObject]@{
                Critère = "Couverture"
                Requis = "≥85%"
                Obtenu = "$coverage%"
                Status = "⚠️ Partiel"
            }
            $totalPoints += 0.5
        } else {
            Write-Host "  ❌ Couverture insuffisante" -ForegroundColor Red
            $results += [PSCustomObject]@{
                Critère = "Couverture"
                Requis = "≥85%"
                Obtenu = "$coverage%"
                Status = "❌ Faible"
            }
        }
    } else {
        Write-Host "  ⚠️ Impossible de lire la couverture" -ForegroundColor Yellow
        $results += [PSCustomObject]@{
            Critère = "Couverture"
            Requis = "≥85%"
            Obtenu = "Non mesurable"
            Status = "⚠️ Inconnu"
        }
    }
} catch {
    Write-Host "  ❌ Erreur pytest: $($_.Exception.Message)" -ForegroundColor Red
    $results += [PSCustomObject]@{
        Critère = "Couverture"
        Requis = "≥85%"
        Obtenu = "Erreur"
        Status = "❌ Échec"
    }
}
Write-Host ""

# ═══════════════════════════════════════════════════════════════
# RÉSUMÉ FINAL
# ═══════════════════════════════════════════════════════════════
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "📊 RÉSULTATS FINAUX - PARTIE 5: TESTS UNITAIRES" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════`n" -ForegroundColor Yellow

$results | Format-Table -AutoSize

Write-Host "`n🎯 SCORE PARTIE 5: $totalPoints / $maxPoints points" -ForegroundColor $(if ($totalPoints -eq $maxPoints) { "Green" } elseif ($totalPoints -ge 3) { "Yellow" } else { "Red" })

if ($totalPoints -eq $maxPoints) {
    Write-Host "`n🎉 PARFAIT! Tous les critères de tests sont remplis!" -ForegroundColor Green
    Write-Host "✅ Conformité totale à la Partie 5 ESG MBA" -ForegroundColor Green
} elseif ($totalPoints -ge 3) {
    Write-Host "`n⚠️ Bon travail! Quelques améliorations possibles" -ForegroundColor Yellow
} else {
    Write-Host "`n❌ Des améliorations sont nécessaires" -ForegroundColor Red
}

Write-Host "`n═══════════════════════════════════════════════════════════════`n" -ForegroundColor Yellow

# Afficher détails des tests
Write-Host "📋 DÉTAILS DES TESTS:" -ForegroundColor Cyan
Write-Host "  • Tests totaux: $totalTests" -ForegroundColor Gray
Write-Host "  • Tests services: $serviceTests (stats: $statsTests, fraude: $fraudTests)" -ForegroundColor Gray
Write-Host "  • Fichiers de test: $($testFiles.Count)" -ForegroundColor Gray

if ($totalPoints -eq $maxPoints) {
    exit 0
} else {
    exit 1
}
