"""
Tests unitaires pour les routes système.

Ce module teste toutes les routes de l'endpoint /api/system.
"""

from fastapi.testclient import TestClient


class TestSystemRoutes:
    """Tests des routes système."""

    def test_get_health(self, client: TestClient) -> None:
        """
        Teste l'endpoint de santé du système.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/system/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "uptime" in data
        assert "dataset_loaded" in data
        assert "total_records" in data
        assert data["status"] in ["ok", "degraded", "error"]
        assert data["dataset_loaded"] is True

    def test_get_metadata(self, client: TestClient) -> None:
        """
        Teste l'endpoint des métadonnées.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/api/system/metadata")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "last_update" in data
        assert "api_name" in data
        assert "python_version" in data
        assert data["version"] == "1.0.0"

    def test_root_endpoint(self, client: TestClient) -> None:
        """
        Teste l'endpoint racine.

        Parameters
        ----------
        client : TestClient
            Client de test FastAPI
        """
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
