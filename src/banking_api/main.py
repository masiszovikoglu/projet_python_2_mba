"""
Application principale FastAPI.

Ce module initialise et configure l'application FastAPI avec toutes
les routes et middlewares nécessaires.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from pathlib import Path

from banking_api.config import settings
from banking_api.data_manager import data_manager
from banking_api.routes import transactions, stats, fraud, customers, system

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Crée et configure l'application FastAPI.

    Returns
    -------
    FastAPI
        Instance de l'application configurée
    """
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description=settings.API_DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configuration CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Enregistrement des routes
    app.include_router(transactions.router)
    app.include_router(stats.router)
    app.include_router(fraud.router)
    app.include_router(customers.router)
    app.include_router(system.router)

    # Gestionnaire d'exceptions global
    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """
        Gestionnaire global des exceptions.

        Parameters
        ----------
        request : Request
            Requête HTTP
        exc : Exception
            Exception levée

        Returns
        -------
        JSONResponse
            Réponse d'erreur formatée
        """
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
                "detail": str(exc),
            },
        )

    # Event handlers
    @app.on_event("startup")
    async def startup_event() -> None:
        """
        Événement exécuté au démarrage de l'application.

        Charge les données depuis le fichier CSV.
        """
        logger.info("Starting Banking Transactions API")
        try:
            if settings.DATA_PATH:
                data_path = Path(settings.DATA_PATH)
                if data_path.exists():
                    data_manager.load_data(str(data_path))
                    logger.info(
                        f"Data loaded: {data_manager.get_record_count()} transactions"
                    )
                else:
                    logger.warning(
                        f"Data file not found: {settings.DATA_PATH}. "
                        "API will run without data."
                    )
            else:
                logger.warning("No data path configured")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")

    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        """
        Événement exécuté à l'arrêt de l'application.
        """
        logger.info("Shutting down Banking Transactions API")

    # Route racine
    @app.get("/", tags=["Root"])
    async def root() -> dict:
        """
        Endpoint racine de l'API.

        Returns
        -------
        dict
            Message de bienvenue
        """
        return {
            "message": "Banking Transactions API",
            "version": settings.API_VERSION,
            "docs": "/docs",
            "redoc": "/redoc",
        }

    return app


def start_server() -> None:
    """
    Démarre le serveur uvicorn.

    Cette fonction est utilisée comme point d'entrée pour la commande
    banking-api définie dans pyproject.toml.
    """
    import uvicorn

    uvicorn.run(
        "banking_api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False,
    )


# Instance de l'application
app = create_app()
