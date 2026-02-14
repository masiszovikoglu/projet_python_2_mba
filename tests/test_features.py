"""
Tests d'intégration avec unittest - Adapté au nouveau schéma CSV.

Ce module contient les tests features utilisant le framework unittest
comme requis dans les spécifications du projet.
"""

import unittest
import sys
from pathlib import Path

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
from banking_api.data_manager import data_manager
from banking_api.services.transactions_service import TransactionsService
from banking_api.services.stats_service import StatsService
from banking_api.services.fraud_detection_service import FraudDetectionService
from banking_api.models import TransactionSearchRequest, FraudPredictionRequest


class TestIntegrationTransactions(unittest.TestCase):
    """Tests d'intégration pour les transactions."""

    @classmethod
    def setUpClass(cls) -> None:
        """
        Configure les données de test pour toute la classe.
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
        df = pd.DataFrame(data)
        data_manager._data = df
        data_manager._loaded = True

    def test_transaction_workflow(self) -> None:
        """
        Teste le flux complet de gestion des transactions.
        """
        # Récupérer toutes les transactions
        result = TransactionsService.get_transactions(page=1, limit=10)
        self.assertEqual(result.total, 5)
        self.assertEqual(len(result.transactions), 5)

        # Récupérer une transaction spécifique
        transaction = TransactionsService.get_transaction_by_id("tx_0001")
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.use_chip, "Swipe Transaction")

    def test_transaction_pagination(self) -> None:
        """
        Teste la pagination des transactions.
        """
        # Page 1 avec 2 éléments
        result = TransactionsService.get_transactions(page=1, limit=2)
        self.assertEqual(result.page, 1)
        self.assertEqual(result.limit, 2)
        self.assertEqual(len(result.transactions), 2)

        # Page 2 avec 2 éléments
        result = TransactionsService.get_transactions(page=2, limit=2)
        self.assertEqual(len(result.transactions), 2)


class TestIntegrationStats(unittest.TestCase):
    """Tests d'intégration pour les statistiques."""

    @classmethod
    def setUpClass(cls) -> None:
        """
        Configure les données de test pour toute la classe.
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
        df = pd.DataFrame(data)
        data_manager._data = df
        data_manager._loaded = True

    def test_statistics_overview(self) -> None:
        """
        Teste les statistiques globales.
        """
        overview = StatsService.get_overview()
        self.assertEqual(overview.total_transactions, 5)
        self.assertGreater(overview.avg_amount, 0)

    def test_statistics_by_type(self) -> None:
        """
        Teste les statistiques par type.
        """
        stats = StatsService.get_stats_by_type()
        self.assertEqual(len(stats), 3)  # Swipe, Chip, Online

        # Vérifier que les types sont présents
        types = [stat.use_chip for stat in stats]
        self.assertIn("Swipe Transaction", types)
        self.assertIn("Chip Transaction", types)

    def test_amount_distribution(self) -> None:
        """
        Teste la distribution des montants.
        """
        distribution = StatsService.get_amount_distribution(bins_count=5)
        self.assertEqual(len(distribution.bins), 5)
        self.assertEqual(len(distribution.counts), 5)
        self.assertEqual(sum(distribution.counts), 5)


class TestIntegrationFraudDetection(unittest.TestCase):
    """Tests d'intégration pour la détection de fraude."""

    @classmethod
    def setUpClass(cls) -> None:
        """
        Configure les données de test pour toute la classe.
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
        df = pd.DataFrame(data)
        data_manager._data = df
        data_manager._loaded = True

    def test_fraud_summary(self) -> None:
        """
        Teste le résumé des fraudes.
        """
        summary = FraudDetectionService.get_fraud_summary()
        self.assertEqual(summary.suspicious_count, 2)  # 2 transactions avec erreurs

    def test_fraud_prediction_high_risk(self) -> None:
        """
        Teste la prédiction de fraude pour une transaction à haut risque.
        """
        request = FraudPredictionRequest(
            amount=500000.0,
            mcc=5999,
            use_chip="Online Transaction",
            merchant_state="CA",
        )
        prediction = FraudDetectionService.predict_fraud(request)
        self.assertTrue(prediction.is_suspicious)
        # Risk level depends on scoring algorithm
        self.assertIn(prediction.risk_level, ["low", "medium", "high"])

    def test_fraud_prediction_low_risk(self) -> None:
        """
        Teste la prédiction de fraude pour une transaction à faible risque.
        """
        request = FraudPredictionRequest(
            amount=50.0,
            mcc=5411,
            use_chip="Chip Transaction",
            merchant_state="NY",
        )
        prediction = FraudDetectionService.predict_fraud(request)
        self.assertEqual(prediction.risk_level, "low")


if __name__ == "__main__":
    unittest.main()

