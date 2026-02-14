"""
Tests unitaires pour les routes de détection de fraude.

Ce module teste toutes les routes de l'endpoint /api/fraud.
"""

from fastapi.testclient import TestClient


class TestFraudRoutes:
    """Tests des routes de détection de fraude."""

    def test_get_fraud_summary(self, client: TestClient) -> None:
        """
        Teste le résumé des fraudes.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/fraud/summary")
        assert response.status_code == 200
        data = response.json()
        assert "suspicious_count" in data
        assert "high_risk_count" in data
        assert "avg_risk_score" in data
        assert "suspicious_rate" in data
        assert data["suspicious_count"] == 2

    def test_get_fraud_by_type(self, client: TestClient) -> None:
        """
        Teste les statistiques de fraude par type.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/fraud/by-type")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        for item in data:
            assert "type" in item
            assert "total_count" in item
            assert "fraud_count" in item
            assert "fraud_rate" in item

    def test_predict_fraud(self, client: TestClient) -> None:
        """
        Teste la prédiction de fraude.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        prediction_payload = {
            "amount": 3500.0,
            "mcc": 5999,
            "use_chip": "Online Transaction",
            "merchant_state": "CA",
        }
        response = client.post("/api/fraud/predict", json=prediction_payload)
        assert response.status_code == 200
        data = response.json()
        assert "is_suspicious" in data
        assert "risk_score" in data
        assert "risk_level" in data
        assert isinstance(data["is_suspicious"], bool)
        assert 0 <= data["risk_score"] <= 100

    def test_predict_fraud_low_risk(self, client: TestClient) -> None:
        """
        Teste la prédiction pour une transaction à faible risque.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        prediction_payload = {
            "amount": 50.0,
            "mcc": 5411,
            "use_chip": "Chip Transaction",
            "merchant_state": "NY",
        }
        response = client.post("/api/fraud/predict", json=prediction_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["risk_level"] in ["low", "medium", "high"]
