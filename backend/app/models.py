"""MongoEngine database models for Price Pulse."""

from datetime import datetime, timezone
import mongoengine as db


class Product(db.Document):
    """Product catalog."""
    meta = {'collection': 'products'}

    id = db.IntField(primary_key=True)
    name = db.StringField(required=True)
    category = db.StringField(required=True)
    brand = db.StringField()
    current_price = db.FloatField(required=True)
    cost_price = db.FloatField(required=True)
    description = db.StringField()
    image_url = db.StringField()
    created_at = db.DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = db.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "brand": self.brand,
            "current_price": self.current_price,
            "cost_price": self.cost_price,
            "description": self.description,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class PriceHistory(db.Document):
    """Historical price records for products."""
    meta = {
        'collection': 'price_history',
        'indexes': [
            ('product_id', 'recorded_at')
        ]
    }

    product_id = db.IntField(required=True)
    price = db.FloatField()
    demand_index = db.FloatField()  # 0.0 to 1.0
    recorded_at = db.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": str(self.id),
            "product_id": self.product_id,
            "price": self.price,
            "demand_index": self.demand_index,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None,
        }


class CompetitorPrice(db.Document):
    """Competitor pricing data."""
    meta = {
        'collection': 'competitor_prices',
        'indexes': [
            ('product_id', 'recorded_at')
        ]
    }

    product_id = db.IntField(required=True)
    competitor_name = db.StringField(required=True)
    price = db.FloatField(required=True)
    recorded_at = db.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": str(self.id),
            "product_id": self.product_id,
            "competitor_name": self.competitor_name,
            "price": self.price,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None,
        }
