"""
Routes API pour la gestion des transactions.

Ce module définit les endpoints FastAPI pour consulter,
filtrer et rechercher des transactions bancaires.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from banking_api.models import (
    Transaction,
    TransactionResponse,
    TransactionSearchRequest,
    ErrorResponse,
)
from banking_api.services.transactions_service import TransactionsService

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])


@router.get(
    "",
    response_model=TransactionResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Liste des transactions",
    description="Récupère une liste paginée de transactions avec filtres optionnels",
)
async def get_transactions(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(100, ge=1, le=1000, description="Éléments par page"),
    use_chip: Optional[str] = Query(None, description="Mode de transaction"),
    merchant_state: Optional[str] = Query(None, description="État du commerçant"),
    min_amount: Optional[float] = Query(None, description="Montant minimum"),
    max_amount: Optional[float] = Query(None, description="Montant maximum"),
) -> TransactionResponse:
    """
    Liste paginée des transactions.

    Parameters
    ----------
    skip : int
        Nombre d'éléments à ignorer
    limit : int
        Nombre d'éléments par page
    use_chip : Optional[str]
        Mode de transaction à filtrer
    merchant_state : Optional[str]
        État du commerçant
    min_amount : Optional[float]
        Montant minimum
    max_amount : Optional[float]
        Montant maximum

    Returns
    -------
    TransactionResponse
        Liste paginée de transactions

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        page = (skip // limit) + 1
        return TransactionsService.get_transactions(
            page=page,
            limit=limit,
            use_chip=use_chip,
            merchant_state=merchant_state,
            min_amount=min_amount,
            max_amount=max_amount,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/search",
    response_model=TransactionResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Recherche multicritère",
    description="Recherche des transactions selon plusieurs critères",
)
async def search_transactions(
    search_request: TransactionSearchRequest,
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(100, ge=1, le=1000, description="Éléments par page"),
) -> TransactionResponse:
    """
    Recherche multicritère de transactions.

    Parameters
    ----------
    search_request : TransactionSearchRequest
        Critères de recherche
    skip : int
        Nombre d'éléments à ignorer
    limit : int
        Éléments par page

    Returns
    -------
    TransactionResponse
        Résultats paginés

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        page = (skip // limit) + 1
        return TransactionsService.search_transactions(search_request, page, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/types",
    response_model=List[str],
    responses={500: {"model": ErrorResponse}},
    summary="Types de transactions",
    description="Liste des types de transactions disponibles",
)
async def get_transaction_types() -> List[str]:
    """
    Liste des types de transactions.

    Returns
    -------
    List[str]
        Types de transactions disponibles

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        return TransactionsService.get_transaction_types()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/recent",
    response_model=List[Transaction],
    responses={500: {"model": ErrorResponse}},
    summary="Transactions récentes",
    description="Récupère les N dernières transactions",
)
async def get_recent_transactions(
    limit: int = Query(10, ge=1, le=100, description="Nombre de transactions")
) -> List[Transaction]:
    """
    Transactions récentes.

    Parameters
    ----------
    limit : int
        Nombre de transactions à récupérer

    Returns
    -------
    List[Transaction]
        Dernières transactions

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        return TransactionsService.get_recent_transactions(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/by-customer",
    response_model=List[Transaction],
    responses={500: {"model": ErrorResponse}},
    summary="Transactions par client",
    description="Liste des transactions émises par un client",
)
async def get_transactions_by_customer(
    client_id: int = Query(..., description="Identifiant du client"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre maximum de transactions"),
) -> List[Transaction]:
    """
    Transactions émises par un client.

    Parameters
    ----------
    client_id : int
        Identifiant du client
    limit : int
        Nombre maximum de résultats

    Returns
    -------
    List[Transaction]
        Liste des transactions

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        return TransactionsService.get_transactions_by_customer(str(client_id), limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/to-merchant",
    response_model=List[Transaction],
    responses={500: {"model": ErrorResponse}},
    summary="Transactions vers un commerçant",
    description="Liste des transactions vers un commerçant",
)
async def get_transactions_to_merchant(
    merchant_id: int = Query(..., description="Identifiant du commerçant"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre maximum de transactions"),
) -> List[Transaction]:
    """
    Transactions vers un commerçant.

    Parameters
    ----------
    merchant_id : int
        Identifiant du commerçant
    limit : int
        Nombre maximum de résultats

    Returns
    -------
    List[Transaction]
        Liste des transactions

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        return TransactionsService.get_transactions_to_merchant(str(merchant_id), limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{id}",
    response_model=Transaction,
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Détails d'une transaction",
    description="Récupère les détails d'une transaction par son identifiant",
)
async def get_transaction_by_id(id: str) -> Transaction:
    """
    Détails d'une transaction.

    Parameters
    ----------
    id : str
        Identifiant de la transaction

    Returns
    -------
    Transaction
        Détails de la transaction

    Raises
    ------
    HTTPException
        Si la transaction n'est pas trouvée
    """
    try:
        transaction = TransactionsService.get_transaction_by_id(id)
        if transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{id}",
    response_model=dict,
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Supprimer une transaction",
    description="Supprime une transaction (mode test uniquement)",
)
async def delete_transaction(id: str) -> dict:
    """
    Supprime une transaction.

    Parameters
    ----------
    id : str
        Identifiant de la transaction

    Returns
    -------
    dict
        Message de confirmation

    Raises
    ------
    HTTPException
        Si la transaction n'est pas trouvée
    """
    try:
        deleted = TransactionsService.delete_transaction(id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return {"message": "Transaction deleted successfully", "id": id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
