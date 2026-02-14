"""
Service de gestion des transactions bancaires.

Ce module fournit les fonctions métier pour la consultation,
le filtrage et la recherche de transactions.
"""

from typing import List, Optional
from banking_api.models import (
    Transaction,
    TransactionResponse,
    TransactionSearchRequest,
)
from banking_api.data_manager import data_manager
import logging

logger = logging.getLogger(__name__)


class TransactionsService:
    """
    Service de gestion des transactions.

    Cette classe fournit les opérations métier pour manipuler
    les transactions bancaires.
    """

    @staticmethod
    def get_transactions(
        page: int = 1,
        limit: int = 100,
        use_chip: Optional[str] = None,
        merchant_state: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
    ) -> TransactionResponse:
        """
        Récupère une liste paginée de transactions avec filtres optionnels.

        Parameters
        ----------
        page : int, optional
            Numéro de page (défaut: 1)
        limit : int, optional
            Nombre d'éléments par page (défaut: 100)
        use_chip : Optional[str], optional
            Mode de transaction à filtrer
        merchant_state : Optional[str], optional
            État du commerçant à filtrer
        min_amount : Optional[float], optional
            Montant minimum
        max_amount : Optional[float], optional
            Montant maximum

        Returns
        -------
        TransactionResponse
            Réponse paginée contenant les transactions
        """
        df = data_manager.get_data()

        # Application des filtres
        if use_chip is not None:
            df = df[df["use_chip"] == use_chip]

        if merchant_state is not None:
            df = df[df["merchant_state"] == merchant_state]

        if min_amount is not None:
            df = df[df["amount"] >= min_amount]

        if max_amount is not None:
            df = df[df["amount"] <= max_amount]

        total = len(df)

        # Pagination
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        df_page = df.iloc[start_idx:end_idx]

        # Convert to models
        transactions = [
            Transaction(**row.to_dict()) for _, row in df_page.iterrows()
        ]

        return TransactionResponse(
            page=page, limit=limit, total=total, transactions=transactions
        )

    @staticmethod
    def get_transaction_by_id(transaction_id: str) -> Optional[Transaction]:
        """
        Récupère une transaction par son identifiant.

        Parameters
        ----------
        transaction_id : str
            Identifiant de la transaction

        Returns
        -------
        Optional[Transaction]
            Transaction trouvée ou None
        """
        df = data_manager.get_data()
        result = df[df["id"] == transaction_id]

        if result.empty:
            return None

        return Transaction(**result.iloc[0].to_dict())

    @staticmethod
    def search_transactions(
        search_request: TransactionSearchRequest, page: int = 1, limit: int = 100
    ) -> TransactionResponse:
        """
        Recherche multicritère de transactions.

        Parameters
        ----------
        search_request : TransactionSearchRequest
            Critères de recherche
        page : int, optional
            Numéro de page (défaut: 1)
        limit : int, optional
            Éléments par page (défaut: 100)

        Returns
        -------
        TransactionResponse
            Réponse paginée des résultats
        """
        df = data_manager.get_data()

        # Application des filtres
        if search_request.use_chip is not None:
            df = df[df["use_chip"] == search_request.use_chip]

        if search_request.amount_range is not None:
            df = df[
                (df["amount"] >= search_request.amount_range[0])
                & (df["amount"] <= search_request.amount_range[1])
            ]

        if search_request.client_id is not None:
            df = df[df["client_id"] == search_request.client_id]

        if search_request.merchant_id is not None:
            df = df[df["merchant_id"] == search_request.merchant_id]

        if search_request.merchant_state is not None:
            df = df[df["merchant_state"] == search_request.merchant_state]

        if search_request.mcc is not None:
            df = df[df["mcc"] == search_request.mcc]

        total = len(df)

        # Pagination
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        df_page = df.iloc[start_idx:end_idx]

        transactions = [
            Transaction(**row.to_dict()) for _, row in df_page.iterrows()
        ]

        return TransactionResponse(
            page=page, limit=limit, total=total, transactions=transactions
        )

    @staticmethod
    def get_transaction_types() -> List[str]:
        """
        Récupère la liste des types de transactions disponibles.

        Returns
        -------
        List[str]
            Liste des modes uniques
        """
        df = data_manager.get_data()
        return sorted(df["use_chip"].unique().tolist())

    @staticmethod
    def get_recent_transactions(n: int = 10) -> List[Transaction]:
        """
        Récupère les N dernières transactions du dataset.

        Parameters
        ----------
        n : int, optional
            Nombre de transactions à récupérer (défaut: 10)

        Returns
        -------
        List[Transaction]
            Liste des dernières transactions
        """
        df = data_manager.get_data()
        df_sorted = df.sort_values("date", ascending=False)
        df_recent = df_sorted.head(n)

        return [Transaction(**row.to_dict()) for _, row in df_recent.iterrows()]

    @staticmethod
    def delete_transaction(transaction_id: str) -> bool:
        """
        Supprime une transaction (mode test uniquement).

        Parameters
        ----------
        transaction_id : str
            Identifiant de la transaction

        Returns
        -------
        bool
            True si supprimé, False sinon
        """
        # Note: This function is for testing purposes only
        # In a real environment, it would modify the database
        df = data_manager.get_data()
        exists = not df[df["id"] == transaction_id].empty

        if exists:
            logger.info(f"Transaction {transaction_id} marked for deletion (test mode)")

        return exists

    @staticmethod
    def get_transactions_by_customer(customer_id: str, limit: int = 100) -> List[Transaction]:
        """
        Récupère les transactions émises par un client.

        Parameters
        ----------
        customer_id : str
            Identifiant du client
        limit : int
            Nombre maximum de transactions

        Returns
        -------
        List[Transaction]
            Liste des transactions
        """
        df = data_manager.get_data()
        df_filtered = df[df["client_id"] == int(customer_id)].head(limit)

        return [Transaction(**row.to_dict()) for _, row in df_filtered.iterrows()]

    @staticmethod
    def get_transactions_to_merchant(merchant_id: str, limit: int = 100) -> List[Transaction]:
        """
        Récupère les transactions vers un commerçant.

        Parameters
        ----------
        merchant_id : str
            Identifiant du commerçant
        limit : int
            Nombre maximum de transactions

        Returns
        -------
        List[Transaction]
            Liste des transactions
        """
        df = data_manager.get_data()
        df_filtered = df[df["merchant_id"] == int(merchant_id)].head(limit)

        return [Transaction(**row.to_dict()) for _, row in df_filtered.iterrows()]
