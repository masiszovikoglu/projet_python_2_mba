"""
Routes API pour la gestion des clients.

Ce module définit les endpoints FastAPI pour explorer
les profils et portefeuilles des clients.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from banking_api.models import Customer, CustomerListResponse, ErrorResponse
from banking_api.services.customer_service import CustomerService

router = APIRouter(prefix="/api/customers", tags=["Customers"])


@router.get(
    "",
    response_model=CustomerListResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Liste des clients",
    description="Liste paginée des clients",
)
async def get_customers(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(100, ge=1, le=1000, description="Éléments par page"),
) -> CustomerListResponse:
    """
    Liste paginée des clients.

    Parameters
    ----------
    skip : int
        Nombre d'éléments à ignorer
    limit : int
        Éléments par page

    Returns
    -------
    CustomerListResponse
        Liste paginée de clients

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        page = (skip // limit) + 1
        return CustomerService.get_customers(page, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/top",
    response_model=List[Dict[str, Any]],
    responses={500: {"model": ErrorResponse}},
    summary="Top clients",
    description="Clients avec le plus grand volume de transactions",
)
async def get_top_customers(
    limit: int = Query(10, ge=1, le=100, description="Nombre de clients")
) -> List[Dict[str, Any]]:
    """
    Top clients par volume de transactions.

    Parameters
    ----------
    limit : int
        Nombre de clients à retourner

    Returns
    -------
    List[Dict[str, Any]]
        Liste des top clients

    Raises
    ------
    HTTPException
        Si une erreur se produit
    """
    try:
        top_customers = CustomerService.get_top_customers(limit)
        return [
            {"customer_id": cust_id, "total_amount": amount}
            for cust_id, amount in top_customers
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{customer_id}",
    response_model=Customer,
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Profil client",
    description="Profil détaillé d'un client",
)
async def get_customer_profile(customer_id: int) -> Customer:
    """
    Profil client détaillé.

    Parameters
    ----------
    customer_id : int
        Identifiant du client

    Returns
    -------
    Customer
        Profil du client

    Raises
    ------
    HTTPException
        Si le client n'est pas trouvé
    """
    try:
        customer = CustomerService.get_customer_profile(customer_id)
        if customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
