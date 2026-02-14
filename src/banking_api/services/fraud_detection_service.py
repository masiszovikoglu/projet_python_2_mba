"""
Service de détection de fraude.

Ce module fournit les fonctions d'analyse et de prédiction
de fraude sur les transactions bancaires.
"""

from typing import List, Literal
from banking_api.models import (
    FraudSummary,
    FraudByType,
    FraudPredictionRequest,
    FraudPredictionResponse,
)
from banking_api.data_manager import data_manager
import logging

logger = logging.getLogger(__name__)


class FraudDetectionService:
    """
    Service de détection de fraude.

    Cette classe fournit les fonctions d'analyse de fraude
    et de scoring pour détecter les transactions suspectes.
    """

    @staticmethod
    def get_fraud_summary() -> FraudSummary:
        """
        Calcule un résumé des statistiques de transactions suspectes.

        Returns
        -------
        FraudSummary
            Résumé des transactions suspectes
        """
        df = data_manager.get_data()

        total_transactions = len(df)

        # Suspicious transactions: negative amounts or very high amounts
        suspicious = df[(df["amount"] < 0) | (df["amount"].abs() > 5000)]
        suspicious_count = len(suspicious)

        # High-risk transactions: very negative amounts
        high_risk = df[df["amount"] < -1000]
        high_risk_count = len(high_risk)

        # Average risk score (based on normalized absolute amount)
        avg_risk_score = min(100, float(df["amount"].abs().mean() / 10))

        suspicious_rate = float(suspicious_count / total_transactions) if total_transactions > 0 else 0.0

        return FraudSummary(
            total_transactions=total_transactions,
            suspicious_count=suspicious_count,
            high_risk_count=high_risk_count,
            avg_risk_score=avg_risk_score,
            suspicious_rate=suspicious_rate,
        )

    @staticmethod
    def get_fraud_by_type() -> List[FraudByType]:
        """
        Calcule le taux de transactions suspectes par mode de transaction.

        Returns
        -------
        List[FraudByType]
            Statistiques de suspicion par mode
        """
        df = data_manager.get_data()

        fraud_stats: List[FraudByType] = []

        for chip_type in df["use_chip"].unique():
            df_type = df[df["use_chip"] == chip_type]
            total_count = len(df_type)
            suspicious_count = len(df_type[df_type["amount"] < 0])
            suspicious_rate = float(suspicious_count / total_count) if total_count > 0 else 0.0

            fraud_stats.append(
                FraudByType(
                    use_chip=str(chip_type),
                    total_count=total_count,
                    suspicious_count=suspicious_count,
                    suspicious_rate=suspicious_rate,
                )
            )

        return fraud_stats

    @staticmethod
    def predict_fraud(request: FraudPredictionRequest) -> FraudPredictionResponse:
        """
        Analyse une transaction et calcule son score de risque.

        Cette fonction utilise des règles heuristiques pour détecter
        des patterns suspects dans les transactions.

        Parameters
        ----------
        request : FraudPredictionRequest
            Caractéristiques de la transaction

        Returns
        -------
        FraudPredictionResponse
            Analyse de risque avec score et raisons
        """
        risk_score = 0.0
        reasons = []

        # Rule 1: Negative amount (chargeback/refund)
        if request.amount < 0:
            risk_score += 30
            reasons.append("Negative amount (chargeback/refund)")

        # Rule 2: Very high amount
        if abs(request.amount) > 5000:
            risk_score += 25
            reasons.append("Very high amount")

        # Rule 3: High-risk categories (Cash Services, etc.)
        high_risk_mccs = [6010, 6011, 6050, 6051, 6211, 6538]  # Risky codes
        if request.mcc in high_risk_mccs:
            risk_score += 20
            reasons.append("High-risk merchant category")

        # Rule 4: Online transaction (higher risk)
        if request.use_chip and request.use_chip == "Online Transaction":
            risk_score += 15
            reasons.append("Online transaction (higher risk)")

        # Rule 5: Some states are riskier (demo purposes)
        high_risk_states = ["CA", "NY", "FL"]
        if request.merchant_state and request.merchant_state in high_risk_states:
            risk_score += 10
            reasons.append(f"Merchant in high-risk state ({request.merchant_state})")

        # Normalize score
        risk_score = min(risk_score, 100.0)

        # Determine if suspicious and risk level
        is_suspicious = risk_score >= 50

        risk_level: Literal["low", "medium", "high"]
        if risk_score < 30:
            risk_level = "low"
        elif risk_score < 70:
            risk_level = "medium"
        else:
            risk_level = "high"

        if not reasons:
            reasons.append("No suspicious patterns detected")

        return FraudPredictionResponse(
            is_suspicious=is_suspicious,
            risk_score=risk_score,
            risk_level=risk_level,
            reasons=reasons
        )
