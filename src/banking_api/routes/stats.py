"""
Routes API pour les statistiques.

Ce module définit les endpoints FastAPI pour consulter
les statistiques et agrégations sur les transactions.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from banking_api.models import (
    StatsOverview,
    AmountDistribution,
    StatsByType,
    DailyStats,
    ErrorResponse,
)
from banking_api.services.stats_service import StatsService

router = APIRouter(prefix="/api/stats", tags=["Statistics"])


@router.get(
    "/overview",
    response_model=StatsOverview,
    responses={500: {"model": ErrorResponse}},
    summary="Statistiques globales",
    description="Vue d'ensemble des statistiques du dataset",
)
async def get_overview() -> StatsOverview:
    """
    Statistiques globales du dataset.

    Returns
    -------
    StatsOverview
        Statistiques globales

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        return StatsService.get_overview()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/amount-distribution",
    response_model=AmountDistribution,
    responses={500: {"model": ErrorResponse}},
    summary="Distribution des montants",
    description="Histogramme des montants de transactions",
)
async def get_amount_distribution(
    bins: int = Query(10, ge=5, le=50, description="Nombre de classes")
) -> AmountDistribution:
    """
    Distribution des montants de transactions.

    Parameters
    ----------
    bins : int
        Nombre de classes pour l'histogramme

    Returns
    -------
    AmountDistribution
        Distribution des montants

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        return StatsService.get_amount_distribution(bins)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/by-chip",
    response_model=List[StatsByType],
    responses={500: {"model": ErrorResponse}},
    summary="Statistiques par mode",
    description="Statistiques agrégées par mode de transaction (Swipe/Chip/Online)",
)
async def get_stats_by_type() -> List[StatsByType]:
    """
    Statistiques par mode de transaction.

    Returns
    -------
    List[StatsByType]
        Statistiques pour chaque mode

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        return StatsService.get_stats_by_type()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/daily",
    response_model=List[DailyStats],
    responses={500: {"model": ErrorResponse}},
    summary="Statistiques quotidiennes",
    description="Statistiques agrégées par jour (step)",
)
async def get_daily_stats() -> List[DailyStats]:
    """
    Statistiques quotidiennes.

    Returns
    -------
    List[DailyStats]
        Statistiques pour chaque jour

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        return StatsService.get_daily_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
