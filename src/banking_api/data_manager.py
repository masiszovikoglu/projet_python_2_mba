"""
Gestionnaire de données pour les transactions bancaires.

Ce module gère le chargement et l'accès aux données de transactions.
"""

import pandas as pd
from typing import Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DataManager:
    """
    Gestionnaire singleton pour les données de transactions.

    Cette classe charge et maintient en mémoire le dataset des transactions
    bancaires. Elle fournit un accès thread-safe aux données.

    Attributes
    ----------
    _instance : Optional[DataManager]
        Instance unique du gestionnaire
    _data : Optional[pd.DataFrame]
        DataFrame contenant les transactions
    _loaded : bool
        Indicateur de chargement des données
    """

    _instance: Optional["DataManager"] = None
    _data: Optional[pd.DataFrame] = None
    _loaded: bool = False

    def __new__(cls) -> "DataManager":
        """
        Crée ou retourne l'instance unique du gestionnaire.

        Returns
        -------
        DataManager
            Instance unique du gestionnaire
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_data(self, file_path: str) -> None:
        """
        Charge les données depuis un fichier CSV.

        Parameters
        ----------
        file_path : str
            Chemin vers le fichier CSV

        Raises
        ------
        FileNotFoundError
            Si le fichier n'existe pas
        ValueError
            Si le fichier est invalide
        """
        path = Path(file_path)
        if not path.exists():
            logger.error(f"Data file not found: {file_path}")
            raise FileNotFoundError(f"Data file not found: {file_path}")

        try:
            logger.info(f"Loading data from {file_path}")
            self._data = pd.read_csv(file_path)

            # Convertir l'ID en string
            self._data["id"] = self._data["id"].astype(str)

            # Clean amount (remove "$" and convert to float)
            if self._data["amount"].dtype == object:
                self._data["amount"] = self._data["amount"].str.replace("$", "").astype(float)

            # Convert zip to int (pandas may load it as float)
            if "zip" in self._data.columns:
                self._data["zip"] = self._data["zip"].fillna(0).astype(int)

            # Clean text fields (replace NaN with empty string)
            text_columns = ["use_chip", "merchant_city", "merchant_state"]
            for col in text_columns:
                if col in self._data.columns:
                    self._data[col] = self._data[col].fillna("").astype(str)

            # Handle missing values in errors
            if "errors" in self._data.columns:
                self._data["errors"] = self._data["errors"].fillna("").astype(str)
                self._data.loc[self._data["errors"] == "nan", "errors"] = None

            self._loaded = True
            logger.info(f"Data loaded successfully: {len(self._data)} transactions")

        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise ValueError(f"Error loading data: {str(e)}")

    def get_data(self) -> pd.DataFrame:
        """
        Retourne le DataFrame des transactions.

        Returns
        -------
        pd.DataFrame
            DataFrame contenant les transactions

        Raises
        ------
        RuntimeError
            Si les données ne sont pas chargées
        """
        if not self._loaded or self._data is None:
            raise RuntimeError("Data not loaded. Call load_data() first.")
        return self._data.copy()

    def is_loaded(self) -> bool:
        """
        Vérifie si les données sont chargées.

        Returns
        -------
        bool
            True si les données sont chargées
        """
        return self._loaded

    def get_record_count(self) -> int:
        """
        Retourne le nombre total d'enregistrements.

        Returns
        -------
        int
            Nombre d'enregistrements
        """
        if not self._loaded or self._data is None:
            return 0
        return len(self._data)


# Instance globale du gestionnaire
data_manager: DataManager = DataManager()
