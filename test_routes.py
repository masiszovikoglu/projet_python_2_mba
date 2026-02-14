"""
Script Python pour tester les 20 routes et générer un rapport.

Usage: python test_routes.py
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple

# Configuration
BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 5


class RouteTest:
    """Classe pour représenter un test de route."""

    def __init__(
        self,
        number: int,
        method: str,
        endpoint: str,
        description: str,
        category: str,
        body: Dict = None,
    ):
        """
        Initialise un test de route.

        Parameters
        ----------
        number : int
            Numéro du test (1-20)
        method : str
            Méthode HTTP (GET, POST, DELETE)
        endpoint : str
            Chemin de l'endpoint
        description : str
            Description du test
        category : str
            Catégorie (Transactions, Stats, etc.)
        body : Dict, optional
            Corps de la requête pour POST
        """
        self.number = number
        self.method = method
        self.endpoint = endpoint
        self.description = description
        self.category = category
        self.body = body
        self.status_code = None
        self.success = False
        self.error = None
        self.response_time = None


def test_route(test: RouteTest) -> RouteTest:
    """
    Teste une route et retourne le résultat.

    Parameters
    ----------
    test : RouteTest
        Test à exécuter

    Returns
    -------
    RouteTest
        Test avec les résultats
    """
    url = f"{BASE_URL}{test.endpoint}"
    start_time = time.time()

    try:
        if test.method == "GET":
            response = requests.get(url, timeout=TIMEOUT)
        elif test.method == "POST":
            response = requests.post(
                url, json=test.body, timeout=TIMEOUT
            )
        elif test.method == "DELETE":
            response = requests.delete(url, timeout=TIMEOUT)
        else:
            raise ValueError(f"Méthode non supportée: {test.method}")

        test.response_time = time.time() - start_time
        test.status_code = response.status_code
        test.success = response.status_code == 200

    except Exception as e:
        test.error = str(e)
        test.response_time = time.time() - start_time

    return test


def generate_html_report(tests: List[RouteTest], output_file: str) -> None:
    """
    Génère un rapport HTML des tests.

    Parameters
    ----------
    tests : List[RouteTest]
        Liste des tests effectués
    output_file : str
        Nom du fichier de sortie
    """
    total = len(tests)
    passed = sum(1 for t in tests if t.success)
    failed = total - passed
    note = round((passed / total) * 10, 2)

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport de Test - Banking API</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0 0 10px 0;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-label {{
            color: #666;
            text-transform: uppercase;
            font-size: 0.9em;
        }}
        .success {{ color: #10b981; }}
        .error {{ color: #ef4444; }}
        .note {{ color: #3b82f6; }}
        
        .category {{
            background: white;
            margin-bottom: 20px;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .category-title {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .test-item {{
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #ddd;
            background: #f9f9f9;
            border-radius: 4px;
        }}
        .test-item.success {{
            border-left-color: #10b981;
        }}
        .test-item.error {{
            border-left-color: #ef4444;
        }}
        .test-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        .test-method {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
            color: white;
        }}
        .method-get {{ background: #10b981; }}
        .method-post {{ background: #3b82f6; }}
        .method-delete {{ background: #ef4444; }}
        
        .status-badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }}
        .status-badge.success {{
            background: #d1fae5;
            color: #065f46;
        }}
        .status-badge.error {{
            background: #fee2e2;
            color: #991b1b;
        }}
        .test-details {{
            font-size: 0.95em;
            color: #666;
        }}
        .endpoint {{
            font-family: 'Courier New', monospace;
            background: #e5e7eb;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            color: #666;
            padding: 20px;
            background: white;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏦 Banking Transactions API</h1>
        <h2>Rapport de Test des 20 Routes FastAPI</h2>
        <p>Généré le {datetime.now().strftime("%d/%m/%Y à %H:%M:%S")}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-label">Routes Testées</div>
            <div class="stat-value">{total}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Succès</div>
            <div class="stat-value success">{passed}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Échecs</div>
            <div class="stat-value error">{failed}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Note Finale</div>
            <div class="stat-value note">{note}/10</div>
        </div>
    </div>
"""

    # Grouper par catégorie
    categories = {}
    for test in tests:
        if test.category not in categories:
            categories[test.category] = []
        categories[test.category].append(test)

    # Générer les sections par catégorie
    for category, cat_tests in categories.items():
        cat_passed = sum(1 for t in cat_tests if t.success)
        html += f"""
    <div class="category">
        <div class="category-title">{category} ({cat_passed}/{len(cat_tests)} réussies)</div>
"""
        for test in cat_tests:
            status_class = "success" if test.success else "error"
            status_text = "✓ SUCCÈS" if test.success else "✗ ÉCHEC"
            method_class = f"method-{test.method.lower()}"

            error_html = ""
            if test.error:
                error_html = f'<div style="color: #ef4444; margin-top: 8px;">Erreur: {test.error}</div>'

            response_time = (
                f"{test.response_time*1000:.0f}ms"
                if test.response_time
                else "N/A"
            )

            html += f"""
        <div class="test-item {status_class}">
            <div class="test-header">
                <div>
                    <span class="test-method {method_class}">{test.method}</span>
                    <strong>#{test.number}</strong> - {test.description}
                </div>
                <span class="status-badge {status_class}">{status_text}</span>
            </div>
            <div class="test-details">
                <div>Endpoint: <span class="endpoint">{test.endpoint}</span></div>
                <div>Status: {test.status_code if test.status_code else 'N/A'} | Temps: {response_time}</div>
                {error_html}
            </div>
        </div>
"""
        html += "    </div>\n"

    # Footer
    notation = "10/10 ✅" if passed == 20 else f"{note}/10"
    html += f"""
    <div class="footer">
        <h2>Notation Finale: {notation}</h2>
        <p><strong>Critère:</strong> Routes FastAPI fonctionnelles et sans erreurs</p>
        <p><strong>Points attribués:</strong> {note}/10 points</p>
        {f'<p style="color: #10b981; font-size: 1.2em;">🎉 PARFAIT! Toutes les routes fonctionnent correctement!</p>' if passed == 20 else ''}
        <hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">
        <p>Projet: Banking Transactions API | MBA 2 - ESG</p>
        <p>Documentation: <a href="http://127.0.0.1:8000/docs">Swagger UI</a> | 
           <a href="http://127.0.0.1:8000/redoc">ReDoc</a></p>
    </div>
</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)


def main() -> None:
    """Fonction principale pour lancer tous les tests."""
    print("=" * 60)
    print("  TEST DES 20 ROUTES FASTAPI")
    print("  Banking Transactions API")
    print("=" * 60)
    print()

    # Définir tous les tests
    tests = [
        # TRANSACTIONS (8 routes)
        RouteTest(1, "GET", "/api/transactions", "Liste des transactions", "Transactions"),
        RouteTest(2, "GET", "/api/transactions/tx_0000001", "Détails transaction", "Transactions"),
        RouteTest(3, "POST", "/api/transactions/search", "Recherche multicritère", "Transactions", {"type": "PAYMENT"}),
        RouteTest(4, "GET", "/api/transactions/types", "Types de transactions", "Transactions"),
        RouteTest(5, "GET", "/api/transactions/recent?n=5", "Transactions récentes", "Transactions"),
        RouteTest(6, "DELETE", "/api/transactions/tx_0000001", "Suppression transaction", "Transactions"),
        RouteTest(7, "GET", "/api/transactions/by-customer/C1231006815", "Transactions par client", "Transactions"),
        RouteTest(8, "GET", "/api/transactions/to-customer/M1979787155", "Transactions vers client", "Transactions"),
        # STATISTIQUES (4 routes)
        RouteTest(9, "GET", "/api/stats/overview", "Statistiques globales", "Statistiques"),
        RouteTest(10, "GET", "/api/stats/amount-distribution?bins=10", "Distribution montants", "Statistiques"),
        RouteTest(11, "GET", "/api/stats/by-type", "Statistiques par type", "Statistiques"),
        RouteTest(12, "GET", "/api/stats/daily", "Statistiques quotidiennes", "Statistiques"),
        # FRAUDE (3 routes)
        RouteTest(13, "GET", "/api/fraud/summary", "Résumé des fraudes", "Détection Fraude"),
        RouteTest(14, "GET", "/api/fraud/by-type", "Fraude par type", "Détection Fraude"),
        RouteTest(15, "POST", "/api/fraud/predict", "Prédiction de fraude", "Détection Fraude", 
                 {"type": "TRANSFER", "amount": 3500, "oldbalanceOrg": 15000, "newbalanceOrig": 11500}),
        # CLIENTS (3 routes)
        RouteTest(16, "GET", "/api/customers", "Liste des clients", "Clients"),
        RouteTest(17, "GET", "/api/customers/C1231006815", "Profil client", "Clients"),
        RouteTest(18, "GET", "/api/customers/top?n=5", "Top clients", "Clients"),
        # SYSTÈME (2 routes)
        RouteTest(19, "GET", "/api/system/health", "Santé du système", "Système"),
        RouteTest(20, "GET", "/api/system/metadata", "Métadonnées", "Système"),
    ]

    print("Exécution des tests...\n")

    # Exécuter tous les tests
    for test in tests:
        print(f"[{test.number}/20] Test: {test.description}...", end=" ")
        test_route(test)
        if test.success:
            print("✓ SUCCÈS")
        else:
            print(f"✗ ÉCHEC ({test.error if test.error else test.status_code})")

    # Calculer les résultats
    passed = sum(1 for t in tests if t.success)
    failed = len(tests) - passed
    note = round((passed / len(tests)) * 10, 2)

    print()
    print("=" * 60)
    print("  RÉSULTATS FINAUX")
    print("=" * 60)
    print(f"Routes testées : {len(tests)}")
    print(f"Routes réussies: {passed}/{len(tests)}")
    print(f"Routes échouées: {failed}/{len(tests)}")
    print()
    print(f"NOTE FINALE: {note}/10")
    print("=" * 60)

    # Générer le rapport HTML
    output_file = "rapport_test_routes.html"
    generate_html_report(tests, output_file)
    print(f"\nRapport HTML généré: {output_file}")
    print("Ouvrez ce fichier dans votre navigateur pour voir le rapport détaillé.")


if __name__ == "__main__":
    main()
