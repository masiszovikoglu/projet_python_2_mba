"""
Tests unitaires pour les routes de statistiques.

Ce module teste toutes les routes de l'endpoint /api/stats.
"""

from fastapi.testclient import TestClient


class TestStatsRoutes:
    """Tests des routes de statistiques."""

    def test_get_overview(self, client: TestClient) -> None:
        """
        Teste la récupération des statistiques globales.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/stats/overview")
        assert response.status_code == 200
        data = response.json()
        assert "total_transactions" in data
        assert "fraud_rate" in data
        assert "avg_amount" in data
        assert "most_common_type" in data
        assert data["total_transactions"] == 5

    def test_get_amount_distribution(self, client: TestClient) -> None:
        """
        Teste la récupération de la distribution des montants.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/stats/amount-distribution?bins=5")
        assert response.status_code == 200
        data = response.json()
        assert "bins" in data
        assert "counts" in data
        assert len(data["bins"]) == 5
        assert len(data["counts"]) == 5

    def test_get_stats_by_type(self, client: TestClient) -> None:
        """
        Teste les statistiques par mode de transaction.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/stats/by-chip")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3  # Swipe, Chip, Online
        for stat in data:
            assert "use_chip" in stat
            assert "count" in stat
            assert "avg_amount" in stat

    def test_get_daily_stats(self, client: TestClient) -> None:
        """
        Teste les statistiques quotidiennes.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/stats/daily")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        for stat in data:
            assert "date" in stat  # Changed from "step" to "date"
            assert "count" in stat
            assert "avg_amount" in stat
