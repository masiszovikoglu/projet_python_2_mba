"""Script simple pour tester les 20 routes."""
import requests

BASE = "http://127.0.0.1:8000"

tests = [
    ("GET", f"{BASE}/api/transactions", "1. Liste transactions"),
    ("GET", f"{BASE}/api/transactions/7475327", "2. Détails transaction"),
    ("POST", f"{BASE}/api/transactions/search", "3. Recherche", {"client_id": 1556}),
    ("GET", f"{BASE}/api/transactions/types", "4. Types"),
    ("GET", f"{BASE}/api/transactions/recent?n=5", "5. Récentes"),
    ("DELETE", f"{BASE}/api/transactions/7475327", "6. Suppression"),
    ("GET", f"{BASE}/api/transactions/by-customer/1556", "7. Par client"),
    ("GET", f"{BASE}/api/transactions/to-merchant/59935", "8. Vers marchand"),
    ("GET", f"{BASE}/api/stats/overview", "9. Stats globales"),
    ("GET", f"{BASE}/api/stats/amount-distribution?bins=10", "10. Distribution"),
    ("GET", f"{BASE}/api/stats/by-chip", "11. Stats par chip"),
    ("GET", f"{BASE}/api/stats/daily", "12. Stats quotidiennes"),
    ("GET", f"{BASE}/api/fraud/summary", "13. Résumé fraude"),
    ("GET", f"{BASE}/api/fraud/by-merchant", "14. Fraude par marchand"),
    ("POST", f"{BASE}/api/fraud/predict", "15. Prédiction", {"amount": -500, "mcc": 5499}),
    ("GET", f"{BASE}/api/customers", "16. Liste clients"),
    ("GET", f"{BASE}/api/customers/1556", "17. Profil client"),
    ("GET", f"{BASE}/api/customers/top?n=5", "18. Top clients"),
    ("GET", f"{BASE}/api/system/health", "19. Health"),
    ("GET", f"{BASE}/api/system/metadata", "20. Metadata"),
]

print("\n" + "="*60)
print("  TEST RAPIDE DES 20 ROUTES")
print("="*60 + "\n")

passed = 0
for method, url, desc, *body in tests:
    try:
        if method == "GET":
            r = requests.get(url, timeout=5)
        elif method == "POST":
            r = requests.post(url, json=body[0] if body else {}, timeout=5)
        elif method == "DELETE":
            r = requests.delete(url, timeout=5)
        
        if r.status_code == 200:
            print(f"✓ {desc}")
            passed += 1
        else:
            print(f"✗ {desc} (Status: {r.status_code})")
    except Exception as e:
        print(f"✗ {desc} (Erreur: {str(e)[:50]})")

print(f"\n{'='*60}")
print(f"RÉSULTAT: {passed}/20 routes fonctionnelles")
print(f"NOTE: {round(passed/20*10, 1)}/10")
print(f"{'='*60}\n")
