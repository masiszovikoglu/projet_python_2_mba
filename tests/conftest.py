"""
Configuration des fixtures pytest.

Ce module définit les fixtures communes utilisées dans les tests.
"""

import pytest
import pandas as pd
from fastapi.testclient import TestClient
from banking_api.main import create_app
from banking_api.data_manager import data_manager


@pytest.fixture(scope="session")
def sample_data() -> pd.DataFrame:
    """
    Crée un jeu de données de test.

    Returns
    -------
    pd.DataFrame
        DataFrame de test avec des transactions fictives
    """
    data = {
        "id": ["tx_0001", "tx_0002", "tx_0003", "tx_0004", "tx_0005"],
        "date": ["2019-01-01", "2019-01-01", "2019-01-02", "2019-01-02", "2019-01-03"],
        "client_id": [1231006815, 1666544295, 1305486145, 840083671, 1234567890],
        "card_id": [1, 2, 3, 4, 5],
        "amount": [9839.64, 181.0, 181.0, 52091.28, 1000.0],
        "use_chip": ["Swipe Transaction", "Chip Transaction", "Online Transaction", "Swipe Transaction", "Chip Transaction"],
        "merchant_id": [1, 2, 3, 4, 5],
        "merchant_city": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
        "merchant_state": ["NY", "CA", "IL", "TX", "AZ"],
        "zip": [10001, 90001, 60601, 77001, 85001],
        "mcc": [5411, 5812, 5999, 5311, 5541],
        "errors": ["", "Bad PIN", "Bad PIN", "", ""],
    }
    return pd.DataFrame(data)


@pytest.fixture(scope="session")
def setup_test_data(sample_data: pd.DataFrame) -> None:
    """
    Initialise le data_manager avec des données de test.

    Parameters
    ----------
    sample_data : pd.DataFrame
        DataFrame de test
    """
    data_manager._data = sample_data
    data_manager._loaded = True


@pytest.fixture(scope="function")
def client(setup_test_data: None) -> TestClient:
    """
    Crée un client de test pour l'API.

    Parameters
    ----------
    setup_test_data : None
        Fixture pour initialiser les données

    Returns
    -------
    TestClient
        Client de test FastAPI
    """
    app = create_app()
    return TestClient(app)
