"""
Synthetic dataset generator for Price Pulse.

Generates realistic pricing data with:
- Seasonal trends (sinusoidal patterns)
- Random competitor price fluctuations (random walk)
- Missing data (5-10% randomly nulled)
- Noisy demand signals
- Multiple product categories
"""

import csv
import math
import os
import random
from datetime import datetime, timedelta

import numpy as np

# Seed for reproducibility
random.seed(42)
np.random.seed(42)

CATEGORIES = {
    "Electronics": [
        ("Wireless Bluetooth Headphones", "SoundMax", 79.99, 35.00),
        ("4K Ultra HD Smart TV 55\"", "VisionPro", 549.99, 280.00),
        ("Portable Power Bank 20000mAh", "ChargePlus", 39.99, 15.00),
        ("Mechanical Gaming Keyboard", "KeyForce", 129.99, 52.00),
    ],
    "Clothing": [
        ("Premium Cotton T-Shirt", "UrbanThread", 29.99, 8.00),
        ("Slim Fit Denim Jeans", "DenimCraft", 69.99, 22.00),
        ("Waterproof Running Jacket", "StormGuard", 119.99, 40.00),
        ("Classic Leather Belt", "HideCraft", 44.99, 12.00),
    ],
    "Home & Kitchen": [
        ("Stainless Steel Blender", "BlendMaster", 89.99, 32.00),
        ("Memory Foam Pillow Set", "DreamSoft", 49.99, 14.00),
        ("Non-stick Cookware 10pc Set", "ChefLine", 159.99, 55.00),
        ("Smart LED Desk Lamp", "LumiTech", 59.99, 18.00),
    ],
    "Sports & Outdoors": [
        ("Yoga Mat Premium 6mm", "FlexFit", 34.99, 9.00),
        ("Insulated Water Bottle 1L", "HydroKeep", 24.99, 7.00),
        ("Adjustable Dumbbell Set 25kg", "IronCore", 199.99, 75.00),
        ("Camping Tent 4-Person", "TrailBlazer", 249.99, 90.00),
    ],
    "Books & Media": [
        ("Bestseller Fiction Novel", "PageTurn", 14.99, 4.00),
        ("Programming Reference Guide", "CodePress", 49.99, 12.00),
        ("Noise Cancelling Earbuds", "AudioPure", 59.99, 20.00),
        ("Digital Drawing Tablet", "ArtPad", 89.99, 35.00),
    ],
}

COMPETITORS = ["Amazon", "BestBuy", "Walmart", "Target", "eBay"]

DAYS_OF_HISTORY = 180  # 6 months


def generate_seasonal_factor(day_index: int) -> float:
    """Generate a seasonal multiplier (peaks around day 90 and 180)."""
    return 1.0 + 0.08 * math.sin(2 * math.pi * day_index / 90)


def generate_demand_index(day_index: int, category: str) -> float | None:
    """Generate a demand index between 0 and 1 with noise and occasional nulls."""
    # Base demand varies by category
    base_demand = {
        "Electronics": 0.65,
        "Clothing": 0.55,
        "Home & Kitchen": 0.50,
        "Sports & Outdoors": 0.45,
        "Books & Media": 0.40,
    }
    base = base_demand.get(category, 0.5)

    # Add seasonal component
    seasonal = 0.15 * math.sin(2 * math.pi * day_index / 60)

    # Add noise
    noise = np.random.normal(0, 0.08)

    demand = base + seasonal + noise
    demand = max(0.0, min(1.0, demand))  # Clamp to [0, 1]

    # 7% chance of missing data
    if random.random() < 0.07:
        return None

    return round(demand, 4)


def generate_price_walk(base_price: float, days: int) -> list[float | None]:
    """Generate a random walk of prices around a base price."""
    prices = []
    current = base_price
    for i in range(days):
        seasonal = generate_seasonal_factor(i)
        # Random daily change: -2% to +2%
        change = np.random.normal(0, 0.012) * current
        current = current + change
        current = max(base_price * 0.7, min(base_price * 1.4, current))  # Bound
        price = round(current * seasonal, 2)

        # 5% chance of missing data
        if random.random() < 0.05:
            prices.append(None)
        else:
            prices.append(price)

    return prices


def generate_competitor_prices(base_price: float, days: int) -> dict[str, list[float | None]]:
    """Generate competitor price series with independent random walks."""
    competitor_data = {}
    for comp in COMPETITORS:
        # Each competitor has a different price offset (-15% to +15%)
        offset = np.random.uniform(-0.15, 0.15)
        comp_base = base_price * (1 + offset)
        competitor_data[comp] = generate_price_walk(comp_base, days)
    return competitor_data


def generate_dataset():
    """Generate the full synthetic dataset and write to CSV files."""
    data_dir = os.path.dirname(os.path.abspath(__file__))

    products_rows = []
    price_history_rows = []
    competitor_rows = []

    product_id = 0
    start_date = datetime.now() - timedelta(days=DAYS_OF_HISTORY)

    for category, items in CATEGORIES.items():
        for name, brand, base_price, cost_price in items:
            product_id += 1

            # Generate our price history
            our_prices = generate_price_walk(base_price, DAYS_OF_HISTORY)
            last_valid_price = base_price

            for day_idx, price in enumerate(our_prices):
                date = start_date + timedelta(days=day_idx)
                demand = generate_demand_index(day_idx, category)

                if price is not None:
                    last_valid_price = price

                price_history_rows.append({
                    "product_id": product_id,
                    "price": price,  # May be None (missing data)
                    "demand_index": demand,
                    "recorded_at": date.strftime("%Y-%m-%d"),
                })

            # Generate competitor prices
            comp_prices = generate_competitor_prices(base_price, DAYS_OF_HISTORY)
            for comp_name, comp_series in comp_prices.items():
                for day_idx, price in enumerate(comp_series):
                    if price is not None:  # Only record non-missing
                        date = start_date + timedelta(days=day_idx)
                        competitor_rows.append({
                            "product_id": product_id,
                            "competitor_name": comp_name,
                            "price": price,
                            "recorded_at": date.strftime("%Y-%m-%d"),
                        })

            # Product record uses last known price
            products_rows.append({
                "id": product_id,
                "name": name,
                "category": category,
                "brand": brand,
                "current_price": last_valid_price,
                "cost_price": cost_price,
                "description": f"High quality {name.lower()} from {brand}. Category: {category}.",
            })

    # Write products CSV
    products_file = os.path.join(data_dir, "products.csv")
    with open(products_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "category", "brand", "current_price", "cost_price", "description"])
        writer.writeheader()
        writer.writerows(products_rows)

    # Write price history CSV
    history_file = os.path.join(data_dir, "price_history.csv")
    with open(history_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["product_id", "price", "demand_index", "recorded_at"])
        writer.writeheader()
        writer.writerows(price_history_rows)

    # Write competitor prices CSV
    competitors_file = os.path.join(data_dir, "competitor_prices.csv")
    with open(competitors_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["product_id", "competitor_name", "price", "recorded_at"])
        writer.writeheader()
        writer.writerows(competitor_rows)

    print(f"Generated {len(products_rows)} products")
    print(f"Generated {len(price_history_rows)} price history records")
    print(f"Generated {len(competitor_rows)} competitor price records")
    print(f"Files written to: {data_dir}")

    return products_rows, price_history_rows, competitor_rows


if __name__ == "__main__":
    generate_dataset()
