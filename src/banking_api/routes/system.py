"""
Routes API pour l'administration système.

Ce module définit les endpoints FastAPI pour la supervision
et les métadonnées du système.
"""

from fastapi import APIRouter, HTTPException
from banking_api.models import SystemHealth, SystemMetadata, ErrorResponse
from banking_api.services.system_service import SystemService

router = APIRouter(prefix="/api/system", tags=["System"])


@router.get(
    "/health",
    response_model=SystemHealth,
    responses={500: {"model": ErrorResponse}},
    summary="Santé du système",
    description="Vérifie l'état de santé de l'API",
)
async def get_health() -> SystemHealth:
    """
    État de santé du système.

    Returns
    -------
    SystemHealth
        Informations sur la santé du système

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        return SystemService.get_health()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/metadata",
    response_model=SystemMetadata,
    responses={500: {"model": ErrorResponse}},
    summary="Métadonnées",
    description="Informations sur la version et la configuration",
)
async def get_metadata() -> SystemMetadata:
    """
    Métadonnées du système.

    Returns
    -------
    SystemMetadata
        Métadonnées de l'API

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        return SystemService.get_metadata()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
