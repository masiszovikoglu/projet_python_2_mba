"""
Script de test complet des 20 endpoints FastAPI.
Adapté au dataset Kaggle réel.
"""
import requests
import json
from typing import Dict, List

BASE_URL = "http://127.0.0.1:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def test_endpoint(num: int, method: str, endpoint: str, description: str, 
                  body: Dict = None, expected_status: int = 200) -> bool:
    """Test un endpoint et retourne True si succès."""
    url = f"{BASE_URL}{endpoint}"
    print(f"[{num}/20] {description}...", end=" ", flush=True)
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=20)
        elif method == "POST":
            response = requests.post(url, json=body, timeout=20)
        elif method == "DELETE":
            response = requests.delete(url, timeout=20)
        else:
            print(f"{Colors.RED}✗ Méthode non supportée{Colors.RESET}")
            return False
        
        if response.status_code == expected_status:
            print(f"{Colors.GREEN}✓ OK{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}✗ FAIL (Status: {response.status_code}){Colors.RESET}")
            if response.status_code >= 400:
                try:
                    error = response.json()
                    print(f"    Erreur: {error.get('detail', 'Unknown')[:100]}")
                except:
                    pass
            return False
            
    except requests.exceptions.Timeout:
        print(f"{Colors.RED}✗ TIMEOUT{Colors.RESET}")
        return False
    except Exception as e:
        print(f"{Colors.RED}✗ ERROR: {str(e)[:50]}{Colors.RESET}")
        return False


def main():
    print(f"\n{Colors.CYAN}{'='*70}")
    print("  TEST DES 20 ENDPOINTS FastAPI")
    print("  Banking Transactions API - Dataset Kaggle Adapté")
    print(f"{'='*70}{Colors.RESET}\n")
    
    passed = 0
    failed = 0
    
    # TRANSACTIONS (8 endpoints)
    print(f"{Colors.YELLOW}━━━ TRANSACTIONS (8 endpoints) ━━━{Colors.RESET}")
    
    if test_endpoint(1, "GET", "/api/transactions?limit=5", "Liste transactions"):
        passed += 1
    else:
        failed += 1
    
    if test_endpoint(2, "GET", "/api/transactions/7475327", "Détails transaction"):
        passed += 1
    else:
        failed += 1
    
    if test_endpoint(3, "POST", "/api/transactions/search", "Recherche multicritère",
                     body={"client_id": 1556, "amount_range": [0, 1000]}):
        passed += 1
    else:
        failed += 1
    
    if test_endpoint(4, "GET", "/api/transactions/types", "Types de transactions"):
        passed += 1
    else:
        failed += 1
    
    if test_endpoint(5, "GET", "/api/transactions/recent?n=5", "Transactions récentes"):
        passed += 1
    else:
        failed += 1
    
    if test_endpoint(6, "DELETE", "/api/transactions/7475327", "Suppression transaction"):
        passed += 1
    else:
        failed += 1
    
    if test_endpoint(7, "GET", "/api/transactions/by-customer?client_id=1556", "Transactions par client"):
        passed += 1
    else:
        failed += 1
    
    if test_endpoint(8, "GET", "/api/transactions/to-merchant?merchant_id=59935", "Transactions vers commerçant"):
        passed += 1
    else:
        failed += 1
    
    # STATISTIQUES (4 endpoints)
    print(f"\n{Colors.YELLOW}━━━ STATISTIQUES (4 endpoints) ━━━{Colors.RESET}")
    
    if test_endpoint(9, "GET", "/api/stats/overview", "Vue d'ensemble statistiques"):
        passed += 1
    else:
        failed += 1
    
    if test_endpoint(10, "GET", "/api/stats/amount-distribution?bins=10", "Distribution montants"):
        passed += 1
    else:
        failed += 1
    
    if test_endpoint(11, "GET", "/api/stats/by-chip", "Statistiques par mode"):
        passed += 1
    else:
        failed += 1
    
    if test_endpoint(12, "GET", "/api/stats/daily", "Statistiques quotidiennes"):
        passed += 1
    else:
        failed += 1
    
    # DÉTECTION DE FRAUDE (3 endpoints)
    print(f"\n{Colors.YELLOW}━━━ DÉTECTION DE FRAUDE (3 endpoints) ━━━{Colors.RESET}")
    
    if test_endpoint(13, "GET", "/api/fraud/summary", "Résumé des fraudes"):
        passed += 1
    else:
        failed += 1
    
    if test_endpoint(14, "GET", "/api/fraud/by-merchant", "Fraude par mode"):
        passed += 1
    else:
        failed += 1
    
    if test_endpoint(15, "POST", "/api/fraud/predict", "Prédiction de fraude",
                     body={"amount": -500, "mcc": 5499}):
        passed += 1
    else:
        failed += 1
    
    # CLIENTS (3 endpoints)
    print(f"\n{Colors.YELLOW}━━━ CLIENTS (3 endpoints) ━━━{Colors.RESET}")
    
    if test_endpoint(16, "GET", "/api/customers?limit=10", "Liste des clients"):
        passed += 1
    else:
        failed += 1
    
    if test_endpoint(17, "GET", "/api/customers/1556", "Profil client"):
        passed += 1
    else:
        failed += 1
    
    if test_endpoint(18, "GET", "/api/customers/top?n=5", "Top clients"):
        passed += 1
    else:
        failed += 1
    
    # SYSTÈME (2 endpoints)
    print(f"\n{Colors.YELLOW}━━━ SYSTÈME (2 endpoints) ━━━{Colors.RESET}")
    
    if test_endpoint(19, "GET", "/api/system/health", "Santé du système"):
        passed += 1
    else:
        failed += 1
    
    if test_endpoint(20, "GET", "/api/system/metadata", "Métadonnées"):
        passed += 1
    else:
        failed += 1
    
    # RÉSULTATS
    print(f"\n{Colors.CYAN}{'='*70}")
    print("  RÉSULTATS FINAUX")
    print(f"{'='*70}{Colors.RESET}")
    print(f"\n{Colors.WHITE}Total testé    : 20 endpoints{Colors.RESET}")
    print(f"{Colors.GREEN}Réussis        : {passed}/20{Colors.RESET}")
    print(f"{Colors.RED}Échoués        : {failed}/20{Colors.RESET}")
    
    note = round((passed / 20) * 10, 1)
    print(f"\n{Colors.CYAN}{'='*70}")
    if passed == 20:
        print(f"{Colors.GREEN}  🎉 NOTE FINALE: {note}/10 - PARFAIT!{Colors.RESET}")
    elif passed >= 15:
        print(f"{Colors.GREEN}  ✓ NOTE FINALE: {note}/10 - TRÈS BIEN!{Colors.RESET}")
    elif passed >= 10:
        print(f"{Colors.YELLOW}  ⚠ NOTE FINALE: {note}/10 - BIEN{Colors.RESET}")
    else:
        print(f"{Colors.RED}  ✗ NOTE FINALE: {note}/10 - À AMÉLIORER{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")
    
    print(f"{Colors.WHITE}Documentation interactive:{Colors.RESET}")
    print(f"  • Swagger UI: {Colors.CYAN}http://127.0.0.1:8000/docs{Colors.RESET}")
    print(f"  • ReDoc:      {Colors.CYAN}http://127.0.0.1:8000/redoc{Colors.RESET}\n")


if __name__ == "__main__":
    main()
