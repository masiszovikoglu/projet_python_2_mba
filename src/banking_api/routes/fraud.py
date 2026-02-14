"""
Routes API pour la détection de fraude.

Ce module définit les endpoints FastAPI pour l'analyse
et la prédiction de fraude.
"""

from fastapi import APIRouter, HTTPException
from typing import List
from banking_api.models import (
    FraudSummary,
    FraudByType,
    FraudPredictionRequest,
    FraudPredictionResponse,
    ErrorResponse,
)
from banking_api.services.fraud_detection_service import FraudDetectionService

router = APIRouter(prefix="/api/fraud", tags=["Fraud Detection"])


@router.get(
    "/summary",
    response_model=FraudSummary,
    responses={500: {"model": ErrorResponse}},
    summary="Résumé des fraudes",
    description="Vue d'ensemble des statistiques de fraude",
)
async def get_fraud_summary() -> FraudSummary:
    """
    Résumé des fraudes.

    Returns
    -------
    FraudSummary
        Statistiques de fraude

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        return FraudDetectionService.get_fraud_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/by-merchant",
    response_model=List[FraudByType],
    responses={500: {"model": ErrorResponse}},
    summary="Fraude par mode",
    description="Taux de transactions suspectes par mode (Swipe/Chip/Online)",
)
async def get_fraud_by_type() -> List[FraudByType]:
    """
    Transactions suspectes par mode.

    Returns
    -------
    List[FraudByType]
        Statistiques de suspicion par mode

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        return FraudDetectionService.get_fraud_by_type()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/predict",
    response_model=FraudPredictionResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Prédiction de fraude",
    description="Prédit si une transaction est frauduleuse",
)
async def predict_fraud(
    request: FraudPredictionRequest,
) -> FraudPredictionResponse:
    """
    Prédiction de fraude.

    Parameters
    ----------
    request : FraudPredictionRequest
        Caractéristiques de la transaction

    Returns
    -------
    FraudPredictionResponse
        Prédiction avec probabilité

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        return FraudDetectionService.predict_fraud(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
