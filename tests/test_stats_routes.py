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
        Teste les statistiques par type de transaction.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/stats/by-type")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 5
        for stat in data:
            assert "type" in stat
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
            assert "step" in stat
            assert "count" in stat
            assert "avg_amount" in stat
