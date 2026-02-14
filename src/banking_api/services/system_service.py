"""
Service système pour la supervision et les métadonnées.

Ce module fournit les informations sur l'état de santé du système
et les métadonnées de l'API.
"""

import sys
import time
from datetime import datetime, timezone
from typing import Literal
from banking_api.models import SystemHealth, SystemMetadata
from banking_api.data_manager import data_manager
from banking_api.config import settings
import logging

logger = logging.getLogger(__name__)

# Application startup timestamp
_start_time: float = time.time()


class SystemService:
    """
    Service de supervision système.

    Cette classe fournit les informations sur l'état de santé
    et les métadonnées de l'API.
    """

    @staticmethod
    def get_health() -> SystemHealth:
        """
        Vérifie l'état de santé de l'API.

        Returns
        -------
        SystemHealth
            État de santé du système
        """
        # Calculer l'uptime
        uptime_seconds = time.time() - _start_time
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        uptime_str = f"{hours}h {minutes}min"

        # Check if dataset is loaded
        dataset_loaded = data_manager.is_loaded()

        # Determine status
        status: Literal["ok", "degraded", "error"] = "ok" if dataset_loaded else "degraded"

        # Obtenir le nombre d'enregistrements
        total_records = data_manager.get_record_count()

        return SystemHealth(
            status=status,
            uptime=uptime_str,
            dataset_loaded=dataset_loaded,
            total_records=total_records,
        )

    @staticmethod
    def get_metadata() -> SystemMetadata:
        """
        Récupère les métadonnées du système.

        Returns
        -------
        SystemMetadata
            Métadonnées de l'API
        """
        # Last update date (current timestamp)
        last_update = datetime.now(timezone.utc).isoformat()

        # Version Python
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

        return SystemMetadata(
            version=settings.API_VERSION,
            last_update=last_update,
            api_name=settings.API_TITLE,
            python_version=python_version,
        )
