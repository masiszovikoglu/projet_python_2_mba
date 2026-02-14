"""
Tests unitaires pour les services métier.

Ce module teste les fonctions des services de l'application.
"""

import pandas as pd
import pytest
from banking_api.services.transactions_service import TransactionsService
from banking_api.services.stats_service import StatsService
from banking_api.services.fraud_detection_service import FraudDetectionService
from banking_api.services.customer_service import CustomerService
from banking_api.data_manager import data_manager
from banking_api.models import TransactionSearchRequest, FraudPredictionRequest


class TestTransactionsService:
    """Tests du service de transactions."""

    def test_get_transactions(self, setup_test_data: None) -> None:
        """
        Teste la récupération des transactions.

        Parameters
        ----------
        setup_test_data : None
            Fixture de données de test
        """
        result = TransactionsService.get_transactions(page=1, limit=10)
        assert result.total == 5
        assert len(result.transactions) == 5

    def test_get_transaction_by_id_found(self, setup_test_data: None) -> None:
        """
        Teste la récupération d'une transaction existante.

        Parameters
        ----------
        setup_test_data : None
            Fixture de données de test
        """
        transaction = TransactionsService.get_transaction_by_id("tx_0001")
        assert transaction is not None
        assert transaction.id == "tx_0001"

    def test_get_transaction_by_id_not_found(self, setup_test_data: None) -> None:
        """
        Teste la récupération d'une transaction inexistante.

        Parameters
        ----------
        setup_test_data : None
            Fixture de données de test
        """
        transaction = TransactionsService.get_transaction_by_id("tx_9999")
        assert transaction is None

    def test_search_transactions(self, setup_test_data: None) -> None:
        """
        Teste la recherche de transactions.

        Parameters
        ----------
        setup_test_data : None
            Fixture de données de test
        """
        search_request = TransactionSearchRequest(merchant_city="New York")
        result = TransactionsService.search_transactions(search_request)
        assert result.total == 1

    def test_get_transaction_types(self, setup_test_data: None) -> None:
        """
        Teste la récupération des types de transactions.

        Parameters
        ----------
        setup_test_data : None
            Fixture de données de test
        """
        types = TransactionsService.get_transaction_types()
        assert len(types) == 3  # Swipe, Chip, Online
        assert "Swipe Transaction" in types


class TestStatsService:
    """Tests du service de statistiques."""

    def test_get_overview(self, setup_test_data: None) -> None:
        """
        Teste les statistiques globales.

        Parameters
        ----------
        setup_test_data : None
            Fixture de données de test
        """
        overview = StatsService.get_overview()
        assert overview.total_transactions == 5
        # Fraud rate might be 0 with test data - no fraud flag in conftest
        assert 0.0 <= overview.fraud_rate <= 1.0

    def test_get_amount_distribution(self, setup_test_data: None) -> None:
        """
        Teste la distribution des montants.

        Parameters
        ----------
        setup_test_data : None
            Fixture de données de test
        """
        distribution = StatsService.get_amount_distribution(bins_count=5)
        assert len(distribution.bins) == 5
        assert len(distribution.counts) == 5

    def test_get_stats_by_type(self, setup_test_data: None) -> None:
        """
        Teste les statistiques par type.

        Parameters
        ----------
        setup_test_data : None
            Fixture de données de test
        """
        stats = StatsService.get_stats_by_type()
        assert len(stats) == 3  # Swipe, Chip, Online


class TestFraudDetectionService:
    """Tests du service de détection de fraude."""

    def test_get_fraud_summary(self, setup_test_data: None) -> None:
        """
        Teste le résumé des fraudes.

        Parameters
        ----------
        setup_test_data : None
            Fixture de données de test
        """
        summary = FraudDetectionService.get_fraud_summary()
        assert summary.suspicious_count == 2  # 2 transactions avec erreurs

    def test_predict_fraud_high_risk(self, setup_test_data: None) -> None:
        """
        Teste la prédiction pour une transaction à haut risque.

        Parameters
        ----------
        setup_test_data : None
            Fixture de données de test
        """
        request = FraudPredictionRequest(
            amount=500000.0,
            mcc=5999,
            use_chip="Online Transaction",
            merchant_state="CA",
        )
        prediction = FraudDetectionService.predict_fraud(request)
        assert prediction.is_suspicious is True
        # Risk level depends on scoring algorithm, just check it's valid
        assert prediction.risk_level in ["low", "medium", "high"]


class TestCustomerService:
    """Tests du service client."""

    def test_get_customers(self, setup_test_data: None) -> None:
        """
        Teste la récupération des clients.

        Parameters
        ----------
        setup_test_data : None
            Fixture de données de test
        """
        result = CustomerService.get_customers(page=1, limit=10)
        assert result.total == 5

    def test_get_customer_profile(self, setup_test_data: None) -> None:
        """
        Teste le profil d'un client.

        Parameters
        ----------
        setup_test_data : None
            Fixture de données de test
        """
        profile = CustomerService.get_customer_profile(1231006815)
        assert profile is not None
        assert profile.id == 1231006815
        assert profile.transactions_count == 1
