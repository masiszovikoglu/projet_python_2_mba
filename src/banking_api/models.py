"""
Modèles de données pour l'API Banking Transactions.

Ce module contient tous les modèles Pydantic utilisés pour la validation
et la sérialisation des données dans l'API REST.
"""

from typing import Optional, List, Literal
from pydantic import BaseModel, Field, field_validator


class Transaction(BaseModel):
    """
    Modèle représentant une transaction bancaire.

    Attributes
    ----------
    id : str
        Identifiant unique de la transaction
    date : str
        Date et heure de la transaction
    client_id : int
        Identifiant du client
    card_id : int
        Identifiant de la carte
    amount : float
        Montant de la transaction
    use_chip : str
        Mode d'utilisation (Swipe Transaction, Chip Transaction, Online Transaction)
    merchant_id : int
        Identifiant du commerçant
    merchant_city : str
        Ville du commerçant
    merchant_state : str
        État du commerçant
    zip : int
        Code postal
    mcc : int
        Code catégorie marchand
    errors : Optional[str]
        Erreurs éventuelles
    """

    id: str = Field(..., description="Transaction unique identifier")
    date: str = Field(..., description="Transaction date and time")
    client_id: int = Field(..., description="Client identifier")
    card_id: int = Field(..., description="Card identifier")
    amount: float = Field(..., description="Transaction amount")
    use_chip: str = Field(..., description="Transaction mode (Swipe/Chip/Online)")
    merchant_id: int = Field(..., description="Merchant identifier")
    merchant_city: str = Field(..., description="Merchant city")
    merchant_state: str = Field(..., description="Merchant state")
    zip: int = Field(..., description="ZIP code")
    mcc: int = Field(..., description="Merchant Category Code")
    errors: Optional[str] = Field(None, description="Transaction errors if any")

    class Config:
        """Configuration Pydantic."""

        json_schema_extra = {
            "example": {
                "id": "7475327",
                "date": "2010-01-01 00:01:00",
                "client_id": 1556,
                "card_id": 2972,
                "amount": -77.00,
                "use_chip": "Swipe Transaction",
                "merchant_id": 59935,
                "merchant_city": "Beula",
                "merchant_state": "TX",
                "zip": 78344,
                "mcc": 5499,
                "errors": None,
            }
        }


class TransactionResponse(BaseModel):
    """
    Réponse paginée pour la liste des transactions.

    Attributes
    ----------
    page : int
        Numéro de page actuel
    limit : int
        Nombre d'éléments par page
    total : int
        Nombre total de transactions
    transactions : List[Transaction]
        Liste des transactions
    """

    page: int = Field(..., ge=1, description="Current page number")
    limit: int = Field(..., ge=1, le=1000, description="Items per page")
    total: int = Field(..., ge=0, description="Total number of transactions")
    transactions: List[Transaction] = Field(..., description="List of transactions")


class TransactionSearchRequest(BaseModel):
    """
    Requête de recherche multicritère pour les transactions.

    Attributes
    ----------
    use_chip : Optional[str]
        Mode de transaction (Swipe/Chip/Online)
    amount_range : Optional[List[float]]
        Plage de montants [min, max]
    client_id : Optional[int]
        Identifiant du client
    merchant_id : Optional[int]
        Identifiant du commerçant
    merchant_state : Optional[str]
        État du commerçant
    mcc : Optional[int]
        Code catégorie marchand
    """

    use_chip: Optional[str] = Field(
        None, description="Transaction mode filter (Swipe Transaction, Chip Transaction, Online Transaction)"
    )
    amount_range: Optional[List[float]] = Field(
        None, min_length=2, max_length=2, description="Amount range [min, max]"
    )
    client_id: Optional[int] = Field(None, description="Client ID filter")
    merchant_id: Optional[int] = Field(None, description="Merchant ID filter")
    merchant_state: Optional[str] = Field(None, description="Merchant state filter")
    mcc: Optional[int] = Field(None, description="Merchant Category Code filter")

    @field_validator("amount_range")
    @classmethod
    def validate_amount_range(cls, v: Optional[List[float]]) -> Optional[List[float]]:
        """
        Valide que la plage de montants est cohérente.

        Parameters
        ----------
        v : Optional[List[float]]
            Plage de montants à valider

        Returns
        -------
        Optional[List[float]]
            Plage validée

        Raises
        ------
        ValueError
            Si min > max
        """
        if v and len(v) == 2 and v[0] > v[1]:
            raise ValueError("amount_range[0] must be <= amount_range[1]")
        return v


class StatsOverview(BaseModel):
    """
    Statistiques globales du dataset.

    Attributes
    ----------
    total_transactions : int
        Nombre total de transactions
    fraud_rate : float
        Taux de fraude
    avg_amount : float
        Montant moyen des transactions
    most_common_type : str
        Type de transaction le plus fréquent
    """

    total_transactions: int = Field(..., description="Total number of transactions")
    fraud_rate: float = Field(..., ge=0, le=1, description="Fraud rate")
    avg_amount: float = Field(..., ge=0, description="Average transaction amount")
    most_common_type: str = Field(..., description="Most common transaction type")


class AmountDistribution(BaseModel):
    """
    Distribution des montants de transactions.

    Attributes
    ----------
    bins : List[str]
        Classes de valeurs
    counts : List[int]
        Nombre de transactions par classe
    """

    bins: List[str] = Field(..., description="Value ranges")
    counts: List[int] = Field(..., description="Count per bin")


class StatsByType(BaseModel):
    """
    Statistiques par mode de transaction.

    Attributes
    ----------
    use_chip : str
        Mode de transaction (Swipe/Chip/Online)
    count : int
        Nombre de transactions
    avg_amount : float
        Montant moyen
    total_amount : float
        Montant total
    """

    use_chip: str = Field(..., description="Transaction mode")
    count: int = Field(..., ge=0, description="Number of transactions")
    avg_amount: float = Field(..., description="Average amount")
    total_amount: float = Field(..., description="Total amount")


class DailyStats(BaseModel):
    """
    Statistiques quotidiennes.

    Attributes
    ----------
    date : str
        Date
    count : int
        Nombre de transactions
    avg_amount : float
        Montant moyen
    total_amount : float
        Montant total
    """

    date: str = Field(..., description="Date")
    count: int = Field(..., ge=0, description="Transaction count")
    avg_amount: float = Field(..., description="Average amount")
    total_amount: float = Field(..., description="Total amount")


class FraudSummary(BaseModel):
    """
    Résumé de la fraude.

    Attributes
    ----------
    total_transactions : int
        Nombre total de transactions
    suspicious_count : int
        Nombre de transactions suspectes
    high_risk_count : int
        Nombre de transactions à haut risque
    avg_risk_score : float
        Score de risque moyen
    suspicious_rate : float
        Taux de transactions suspectes
    """

    total_transactions: int = Field(..., ge=0, description="Total transactions")
    suspicious_count: int = Field(..., ge=0, description="Suspicious transactions")
    high_risk_count: int = Field(..., ge=0, description="High risk transactions")
    avg_risk_score: float = Field(..., ge=0, le=100, description="Average risk score")
    suspicious_rate: float = Field(..., ge=0, le=1, description="Suspicious rate")


class FraudByType(BaseModel):
    """
    Fraude par mode de transaction.

    Attributes
    ----------
    use_chip : str
        Mode de transaction
    total_count : int
        Nombre total de transactions
    suspicious_count : int
        Nombre de transactions suspectes
    suspicious_rate : float
        Taux de transactions suspectes
    """

    use_chip: str = Field(..., description="Transaction mode")
    total_count: int = Field(..., ge=0, description="Total transactions")
    suspicious_count: int = Field(..., ge=0, description="Suspicious transactions")
    suspicious_rate: float = Field(..., ge=0, le=1, description="Suspicious rate")


class FraudPredictionRequest(BaseModel):
    """
    Requête de prédiction de fraude.

    Attributes
    ----------
    amount : float
        Montant de la transaction
    mcc : int
        Code catégorie marchand
    use_chip : Optional[str]
        Mode de transaction
    merchant_state : Optional[str]
        État du commerçant
    """

    amount: float = Field(..., description="Transaction amount")
    mcc: int = Field(..., description="Merchant Category Code")
    use_chip: Optional[str] = Field(None, description="Transaction mode")
    merchant_state: Optional[str] = Field(None, description="Merchant state")


class FraudPredictionResponse(BaseModel):
    """
    Réponse de prédiction de fraude.

    Attributes
    ----------
    is_suspicious : bool
        Transaction suspecte
    risk_score : float
        Score de risque (0-100)
    risk_level : str
        Niveau de risque (low, medium, high)
    reasons : List[str]
        Raisons de la suspicion
    """

    is_suspicious: bool = Field(..., description="Is transaction suspicious")
    risk_score: float = Field(..., ge=0, le=100, description="Risk score (0-100)")
    risk_level: Literal["low", "medium", "high"] = Field(
        ..., description="Risk level"
    )
    reasons: List[str] = Field(..., description="Risk factors detected")


class Customer(BaseModel):
    """
    Profil client.

    Attributes
    ----------
    id : int
        Identifiant du client
    transactions_count : int
        Nombre de transactions
    avg_amount : float
        Montant moyen des transactions
    total_amount : float
        Montant total des transactions
    unique_merchants : int
        Nombre de commerçants uniques
    """

    id: int = Field(..., description="Customer ID")
    transactions_count: int = Field(..., ge=0, description="Number of transactions")
    avg_amount: float = Field(..., description="Average transaction amount")
    total_amount: float = Field(..., description="Total transaction amount")
    unique_merchants: int = Field(..., ge=0, description="Unique merchants count")


class CustomerListResponse(BaseModel):
    """
    Réponse paginée pour la liste des clients.

    Attributes
    ----------
    page : int
        Numéro de page
    limit : int
        Éléments par page
    total : int
        Nombre total de clients
    customers : List[str]
        Liste des identifiants clients
    """

    page: int = Field(..., ge=1, description="Page number")
    limit: int = Field(..., ge=1, le=1000, description="Items per page")
    total: int = Field(..., ge=0, description="Total customers")
    customers: List[str] = Field(..., description="Customer IDs")


class SystemHealth(BaseModel):
    """
    État de santé du système.

    Attributes
    ----------
    status : str
        Statut du système
    uptime : str
        Temps de fonctionnement
    dataset_loaded : bool
        Dataset chargé
    total_records : int
        Nombre total d'enregistrements
    """

    status: Literal["ok", "degraded", "error"] = Field(..., description="System status")
    uptime: str = Field(..., description="System uptime")
    dataset_loaded: bool = Field(..., description="Dataset loaded status")
    total_records: int = Field(..., ge=0, description="Total records in dataset")


class SystemMetadata(BaseModel):
    """
    Métadonnées du système.

    Attributes
    ----------
    version : str
        Version de l'API
    last_update : str
        Date de dernière mise à jour
    api_name : str
        Nom de l'API
    python_version : str
        Version Python
    """

    version: str = Field(..., description="API version")
    last_update: str = Field(..., description="Last update timestamp")
    api_name: str = Field(..., description="API name")
    python_version: str = Field(..., description="Python version")


class ErrorResponse(BaseModel):
    """
    Réponse d'erreur standardisée.

    Attributes
    ----------
    error : str
        Type d'erreur
    message : str
        Message d'erreur
    detail : Optional[str]
        Détails supplémentaires
    """

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional details")
