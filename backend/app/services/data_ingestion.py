"""
Data ingestion service — loads CSV data into the database.

Handles:
- Reading generated CSV files
- Inserting products, price history, and competitor prices
- Handling missing/incomplete data gracefully
"""

import csv
import logging
import os
from datetime import datetime

from app.models import CompetitorPrice, PriceHistory, Product

logger = logging.getLogger(__name__)


def load_csv_data(data_dir: str = None):
    """
    Load CSV data files into the database.

    Args:
        data_dir: Path to directory containing CSV files.
                  Defaults to backend/data/
    """
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")

    data_dir = os.path.abspath(data_dir)

    # Check if data already exists
    existing_count = Product.objects.count()
    if existing_count > 0:
        logger.info(f"Database already contains {existing_count} products. Skipping import.")
        return existing_count

    logger.info(f"Loading data from {data_dir}")

    # Load products
    products_file = os.path.join(data_dir, "products.csv")
    if not os.path.exists(products_file):
        logger.warning(f"Products file not found: {products_file}")
        return 0

    product_count = 0
    batch = []
    with open(products_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = Product(
                id=int(row["id"]),
                name=row["name"],
                category=row["category"],
                brand=row["brand"],
                current_price=float(row["current_price"]),
                cost_price=float(row["cost_price"]),
                description=row.get("description", ""),
            )
            batch.append(product)
            product_count += 1
            if len(batch) >= 500:
                Product.objects.insert(batch)
                batch = []
        if batch:
            Product.objects.insert(batch)

    logger.info(f"Loaded {product_count} products.")

    # Load price history
    history_file = os.path.join(data_dir, "price_history.csv")
    history_count = 0
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            batch = []
            for row in reader:
                price_val = row.get("price", "")
                demand_val = row.get("demand_index", "")

                history = PriceHistory(
                    product_id=int(row["product_id"]),
                    price=float(price_val) if price_val else None,
                    demand_index=float(demand_val) if demand_val else None,
                    recorded_at=datetime.strptime(row["recorded_at"], "%Y-%m-%d"),
                )
                batch.append(history)
                history_count += 1

                if len(batch) >= 500:
                    PriceHistory.objects.insert(batch)
                    batch = []

            if batch:
                PriceHistory.objects.insert(batch)

    logger.info(f"Loaded {history_count} price history records.")

    # Load competitor prices
    comp_file = os.path.join(data_dir, "competitor_prices.csv")
    comp_count = 0
    if os.path.exists(comp_file):
        with open(comp_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            batch = []
            for row in reader:
                comp = CompetitorPrice(
                    product_id=int(row["product_id"]),
                    competitor_name=row["competitor_name"],
                    price=float(row["price"]),
                    recorded_at=datetime.strptime(row["recorded_at"], "%Y-%m-%d"),
                )
                batch.append(comp)
                comp_count += 1

                if len(batch) >= 500:
                    CompetitorPrice.objects.insert(batch)
                    batch = []

            if batch:
                CompetitorPrice.objects.insert(batch)

    logger.info(f"Loaded {comp_count} competitor price records.")
    logger.info("Data ingestion complete.")

    return product_count
