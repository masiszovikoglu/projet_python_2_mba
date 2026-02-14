"""
Service de statistiques pour les transactions bancaires.

Ce module fournit les fonctions de calcul des statistiques
et agrégations sur les données de transactions.
"""

import pandas as pd
import numpy as np
from typing import List
from banking_api.models import (
    StatsOverview,
    AmountDistribution,
    StatsByType,
    DailyStats,
)
from banking_api.data_manager import data_manager
import logging

logger = logging.getLogger(__name__)


class StatsService:
    """
    Service de calcul de statistiques.

    Cette classe fournit les opérations de calcul d'agrégations
    et de statistiques sur les transactions.
    """

    @staticmethod
    def get_overview() -> StatsOverview:
        """
        Calcule les statistiques globales du dataset.

        Returns
        -------
        StatsOverview
            Statistiques globales
        """
        df = data_manager.get_data()

        total_transactions = len(df)
        # Number of negative transactions (possible fraud/refund indicator)
        negative_count = len(df[df["amount"] < 0])
        negative_rate = float(negative_count / total_transactions) if total_transactions > 0 else 0.0
        avg_amount = float(df["amount"].mean())
        most_common_type = str(df["use_chip"].mode()[0]) if len(df) > 0 else "N/A"

        return StatsOverview(
            total_transactions=total_transactions,
            fraud_rate=negative_rate,  # Negative transactions rate
            avg_amount=avg_amount,
            most_common_type=most_common_type,
        )

    @staticmethod
    def get_amount_distribution(bins_count: int = 10) -> AmountDistribution:
        """
        Calcule la distribution des montants de transactions.

        Parameters
        ----------
        bins_count : int, optional
            Nombre de classes (défaut: 10)

        Returns
        -------
        AmountDistribution
            Distribution des montants
        """
        df = data_manager.get_data()

        # Create bins
        max_amount = df["amount"].max()
        bin_edges = np.linspace(0, max_amount, bins_count + 1)

        counts, edges = np.histogram(df["amount"], bins=bin_edges)

        # Formater les labels des bins
        bin_labels = []
        for i in range(len(edges) - 1):
            label = f"{edges[i]:.0f}-{edges[i+1]:.0f}"
            bin_labels.append(label)

        return AmountDistribution(
            bins=bin_labels,
            counts=counts.tolist(),
        )

    @staticmethod
    def get_stats_by_type() -> List[StatsByType]:
        """
        Calcule les statistiques par mode de transaction.

        Returns
        -------
        List[StatsByType]
            Statistiques pour chaque mode
        """
        df = data_manager.get_data()

        stats_list: List[StatsByType] = []

        for chip_type in df["use_chip"].unique():
            df_type = df[df["use_chip"] == chip_type]
            count = len(df_type)
            avg_amount = float(df_type["amount"].mean())
            total_amount = float(df_type["amount"].sum())

            stats_list.append(
                StatsByType(
                    use_chip=str(chip_type),
                    count=count,
                    avg_amount=avg_amount,
                    total_amount=total_amount,
                )
            )

        return stats_list

    @staticmethod
    def get_daily_stats() -> List[DailyStats]:
        """
        Calcule les statistiques quotidiennes (par date).

        Returns
        -------
        List[DailyStats]
            Statistiques pour chaque jour
        """
        df = data_manager.get_data()

        # Extraire la date sans l'heure
        df["date_only"] = pd.to_datetime(df["date"]).dt.date

        # Grouper par date
        grouped = df.groupby("date_only").agg(
            count=("amount", "count"),
            avg_amount=("amount", "mean"),
            total_amount=("amount", "sum"),
        )

        daily_stats: List[DailyStats] = []

        for date, row in grouped.iterrows():
            daily_stats.append(
                DailyStats(
                    date=str(date),
                    count=int(row["count"]),
                    avg_amount=float(row["avg_amount"]),
                    total_amount=float(row["total_amount"]),
                )
            )

        return sorted(daily_stats, key=lambda x: x.date)
