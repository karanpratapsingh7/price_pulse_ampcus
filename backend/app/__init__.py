"""Flask application factory for Price Pulse."""

import logging
from flask import Flask
from flask_cors import CORS
from mongoengine import connect

from config import get_config


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app_config = get_config()
    app.config.from_object(app_config)

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, app_config.LOG_LEVEL, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting Price Pulse API (env=%s)", app.config.get("ENV", "development"))

    # Initialize extensions
    CORS(app, origins=app_config.CORS_ORIGINS)
    connect(host=app_config.MONGODB_SETTINGS['host'])

    # Register blueprints
    from app.routes.products import products_bp
    from app.routes.prices import prices_bp
    from app.routes.predictions import predictions_bp

    app.register_blueprint(products_bp, url_prefix="/api")
    app.register_blueprint(prices_bp, url_prefix="/api")
    app.register_blueprint(predictions_bp, url_prefix="/api")

    # Health check
    @app.route("/api/health")
    def health():
        return {"status": "ok", "service": "price-pulse-api"}

    # Initialize database
    with app.app_context():
        from app import models  # noqa: F401
        logger.info("MongoDB initialized.")

        # Auto-load data if database is empty
        from app.services.data_ingestion import load_csv_data
        load_csv_data()

    return app
