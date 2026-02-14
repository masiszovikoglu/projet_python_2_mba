"""
Service de gestion des clients.

Ce module fournit les fonctions métier pour l'exploration
des portefeuilles clients.
"""

from typing import List, Optional, Tuple
from banking_api.models import Customer, CustomerListResponse
from banking_api.data_manager import data_manager
import logging

logger = logging.getLogger(__name__)


class CustomerService:
    """
    Service de gestion des clients.

    Cette classe fournit les opérations métier pour analyser
    les profils et comportements des clients.
    """

    @staticmethod
    def get_customers(page: int = 1, limit: int = 100) -> CustomerListResponse:
        """
        Récupère une liste paginée des clients.

        Parameters
        ----------
        page : int, optional
            Numéro de page (défaut: 1)
        limit : int, optional
            Éléments par page (défaut: 100)

        Returns
        -------
        CustomerListResponse
            Liste paginée des clients
        """
        df = data_manager.get_data()

        # Récupérer tous les clients uniques (convertir en string)
        customers = sorted(df["client_id"].unique().tolist())
        total = len(customers)

        # Pagination
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        customers_page = [str(c) for c in customers[start_idx:end_idx]]

        return CustomerListResponse(
            page=page, limit=limit, total=total, customers=customers_page
        )

    @staticmethod
    def get_customer_profile(customer_id: int) -> Optional[Customer]:
        """
        Récupère le profil détaillé d'un client.

        Parameters
        ----------
        customer_id : int
            Identifiant du client

        Returns
        -------
        Optional[Customer]
            Profil du client ou None si non trouvé
        """
        df = data_manager.get_data()

        # Récupérer toutes les transactions du client
        df_customer = df[df["client_id"] == customer_id]

        if df_customer.empty:
            return None

        transactions_count = len(df_customer)
        avg_amount = float(df_customer["amount"].mean())
        total_amount = float(df_customer["amount"].sum())
        unique_merchants = int(df_customer["merchant_id"].nunique())

        return Customer(
            id=customer_id,
            transactions_count=transactions_count,
            avg_amount=avg_amount,
            total_amount=total_amount,
            unique_merchants=unique_merchants,
        )

    @staticmethod
    def get_top_customers(n: int = 10) -> List[Tuple[int, float]]:
        """
        Récupère les clients avec le plus grand volume de transactions.

        Parameters
        ----------
        n : int, optional
            Nombre de clients à retourner (défaut: 10)

        Returns
        -------
        List[Tuple[int, float]]
            Liste de tuples (customer_id, total_amount)
        """
        df = data_manager.get_data()

        # Grouper par client et calculer le volume total (en valeur absolue pour inclure remboursements)
        customer_volumes = (
            df.groupby("client_id")["amount"].apply(lambda x: x.abs().sum())
            .sort_values(ascending=False).head(n)
        )

        return [(int(idx), float(val)) for idx, val in customer_volumes.items()]
