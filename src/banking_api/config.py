"""
Configuration de l'application.

Ce module gère les paramètres de configuration de l'API.
"""

import os
from typing import Optional


class Settings:
    """
    Classe de configuration de l'application.

    Attributes
    ----------
    API_TITLE : str
        Titre de l'API
    API_VERSION : str
        Version de l'API
    API_DESCRIPTION : str
        Description de l'API
    DATA_PATH : Optional[str]
        Chemin vers le fichier de données
    MAX_PAGE_SIZE : int
        Taille maximale de page pour la pagination
    DEFAULT_PAGE_SIZE : int
        Taille par défaut de page
    """

    API_TITLE: str = "Banking Transactions API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = (
        "API REST pour l'exposition des données de transactions bancaires"
    )
    DATA_PATH: Optional[str] = os.getenv(
        "DATA_PATH", "data/transactions_data.csv"
    )
    MAX_PAGE_SIZE: int = 1000
    DEFAULT_PAGE_SIZE: int = 100
    HOST: str = os.getenv("API_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("API_PORT", "8000"))


settings: Settings = Settings()
