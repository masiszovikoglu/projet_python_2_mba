"""
Tests unitaires pour les routes de transactions.

Ce module teste toutes les routes de l'endpoint /api/transactions.
"""

import pytest
from fastapi.testclient import TestClient


class TestTransactionsRoutes:
    """Tests des routes de transactions."""

    def test_get_transactions(self, client: TestClient) -> None:
        """
        Teste la récupération de la liste des transactions.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/transactions")
        assert response.status_code == 200
        data = response.json()
        assert "page" in data
        assert "transactions" in data
        assert "total" in data
        assert data["total"] == 5

    def test_get_transactions_with_filters(self, client: TestClient) -> None:
        """
        Teste la récupération avec filtres.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/transactions?type=PAYMENT")
        assert response.status_code == 200
        data = response.json()
        assert len(data["transactions"]) == 1
        assert data["transactions"][0]["type"] == "PAYMENT"

    def test_get_transactions_pagination(self, client: TestClient) -> None:
        """
        Teste la pagination.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/transactions?page=1&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["limit"] == 2
        assert len(data["transactions"]) == 2

    def test_get_transaction_by_id(self, client: TestClient) -> None:
        """
        Teste la récupération d'une transaction par ID.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/transactions/tx_0001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "tx_0001"

    def test_get_transaction_by_id_not_found(self, client: TestClient) -> None:
        """
        Teste la récupération d'une transaction inexistante.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/transactions/tx_9999")
        assert response.status_code == 404

    def test_search_transactions(self, client: TestClient) -> None:
        """
        Teste la recherche multicritère.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        search_payload = {
            "use_chip": "Chip Transaction",
            "merchant_city": "Los Angeles",
        }
        response = client.post("/api/transactions/search", json=search_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["transactions"][0]["use_chip"] == "Chip Transaction"

    def test_get_transaction_types(self, client: TestClient) -> None:
        """
        Teste la récupération des types de transactions.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/transactions/types")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 5

    def test_get_recent_transactions(self, client: TestClient) -> None:
        """
        Teste la récupération des transactions récentes.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/transactions/recent?n=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 3

    def test_delete_transaction(self, client: TestClient) -> None:
        """
        Teste la suppression d'une transaction.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.delete("/api/transactions/tx_0001")
        assert response.status_code == 200

    def test_get_transactions_by_customer(self, client: TestClient) -> None:
        """
        Teste la récupération des transactions par client.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/transactions/by-customer/C1231006815")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_transactions_to_customer(self, client: TestClient) -> None:
        """
        Teste la récupération des transactions vers un client.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/transactions/to-customer/C840083671")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
