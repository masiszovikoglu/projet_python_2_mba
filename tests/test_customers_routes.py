"""
Tests unitaires pour les routes de gestion des clients.

Ce module teste toutes les routes de l'endpoint /api/customers.
"""

from fastapi.testclient import TestClient


class TestCustomersRoutes:
    """Tests des routes de gestion des clients."""

    def test_get_customers(self, client: TestClient) -> None:
        """
        Teste la récupération de la liste des clients.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/customers")
        assert response.status_code == 200
        data = response.json()
        assert "page" in data
        assert "customers" in data
        assert "total" in data
        assert isinstance(data["customers"], list)

    def test_get_customers_pagination(self, client: TestClient) -> None:
        """
        Teste la pagination des clients.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/customers?page=1&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["limit"] == 3

    def test_get_customer_profile(self, client: TestClient) -> None:
        """
        Teste la récupération du profil d'un client.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/customers/1231006815")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "transactions_count" in data
        assert "avg_amount" in data
        assert "total_amount" in data
        assert data["id"] == 1231006815

    def test_get_customer_profile_not_found(self, client: TestClient) -> None:
        """
        Teste la récupération d'un client inexistant.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/customers/9999999999")
        assert response.status_code == 404

    def test_get_top_customers(self, client: TestClient) -> None:
        """
        Teste la récupération des top clients.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/customers/top?n=3")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3  # We asked for top 3
        for customer in data:
            assert "customer_id" in customer
            assert "total_amount" in customer
