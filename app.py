from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime
from typing import Iterable

from flask import Flask, jsonify

DEFAULT_NEAR_EXPIRY_THRESHOLD_DAYS = 30


@dataclass(frozen=True)
class Batch:
    batch_id: str
    product_type: str
    expires_on: date
    available_liters: float


@dataclass(frozen=True)
class ProductTypeThresholdConfig:
    product_type: str
    near_expiry_threshold_days: int


BATCHES: list[Batch] = [
    Batch(batch_id="milk-1", product_type="milk", expires_on=date(2026, 3, 20), available_liters=500),
    Batch(batch_id="milk-2", product_type="milk", expires_on=date(2026, 5, 1), available_liters=250),
    Batch(batch_id="juice-1", product_type="juice", expires_on=date(2026, 4, 5), available_liters=100),
    Batch(batch_id="juice-2", product_type="juice", expires_on=date(2026, 3, 18), available_liters=0),
]

PRODUCT_TYPE_THRESHOLD_CONFIGS: list[ProductTypeThresholdConfig] = []


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.setdefault("TODAY", date.today())
    app.config.setdefault("BATCHES", BATCHES.copy())
    app.config.setdefault("PRODUCT_TYPE_THRESHOLD_CONFIGS", PRODUCT_TYPE_THRESHOLD_CONFIGS.copy())

    @app.get("/near-expiry")
    def near_expiry():
        batches = app.config["BATCHES"]
        configs = app.config["PRODUCT_TYPE_THRESHOLD_CONFIGS"]
        today = _coerce_date(app.config["TODAY"])
        results = [serialize_batch(batch) for batch in get_near_expiry_batches(batches, configs, today)]
        return jsonify(results)

    return app


def _coerce_date(value: date | str) -> date:
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()



def resolve_near_expiry_threshold(product_type: str, configs: Iterable[ProductTypeThresholdConfig]) -> int:
    for config in configs:
        if config.product_type == product_type:
            return config.near_expiry_threshold_days
    return DEFAULT_NEAR_EXPIRY_THRESHOLD_DAYS



def is_near_expiry(batch: Batch, today: date, configs: Iterable[ProductTypeThresholdConfig]) -> bool:
    if batch.available_liters <= 0:
        return False
    threshold_days = resolve_near_expiry_threshold(batch.product_type, configs)
    days_until_expiry = (batch.expires_on - today).days
    return 0 <= days_until_expiry <= threshold_days



def get_near_expiry_batches(
    batches: Iterable[Batch],
    configs: Iterable[ProductTypeThresholdConfig],
    today: date,
) -> list[Batch]:
    return [batch for batch in batches if is_near_expiry(batch, today, configs)]



def serialize_batch(batch: Batch) -> dict[str, object]:
    data = asdict(batch)
    data["expires_on"] = batch.expires_on.isoformat()
    return data


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50282)
