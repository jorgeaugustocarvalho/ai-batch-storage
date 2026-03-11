from datetime import date

from app import (
    Batch,
    ProductTypeThresholdConfig,
    create_app,
    get_near_expiry_batches,
    resolve_near_expiry_threshold,
)


def test_resolve_threshold_uses_default_when_not_configured():
    assert resolve_near_expiry_threshold("milk", []) == 30


def test_resolve_threshold_uses_product_specific_configuration():
    configs = [ProductTypeThresholdConfig(product_type="milk", near_expiry_threshold_days=10)]
    assert resolve_near_expiry_threshold("milk", configs) == 10


def test_get_near_expiry_batches_uses_default_threshold_when_no_configuration_exists():
    batches = [
        Batch(batch_id="milk-1", product_type="milk", expires_on=date(2026, 3, 20), available_liters=100),
        Batch(batch_id="milk-2", product_type="milk", expires_on=date(2026, 4, 20), available_liters=100),
    ]

    results = get_near_expiry_batches(batches, [], today=date(2026, 3, 11))

    assert [batch.batch_id for batch in results] == ["milk-1"]


def test_get_near_expiry_batches_honors_product_type_configuration():
    batches = [
        Batch(batch_id="juice-1", product_type="juice", expires_on=date(2026, 3, 18), available_liters=100),
        Batch(batch_id="juice-2", product_type="juice", expires_on=date(2026, 3, 25), available_liters=100),
    ]
    configs = [ProductTypeThresholdConfig(product_type="juice", near_expiry_threshold_days=10)]

    results = get_near_expiry_batches(batches, configs, today=date(2026, 3, 11))

    assert [batch.batch_id for batch in results] == ["juice-1"]


def test_near_expiry_endpoint_filters_zero_available_liters_and_remains_backward_compatible():
    app = create_app()
    app.config.update(
        TESTING=True,
        TODAY=date(2026, 3, 11),
        BATCHES=[
            Batch(batch_id="milk-1", product_type="milk", expires_on=date(2026, 3, 20), available_liters=100),
            Batch(batch_id="juice-1", product_type="juice", expires_on=date(2026, 3, 18), available_liters=0),
            Batch(batch_id="milk-2", product_type="milk", expires_on=date(2026, 5, 1), available_liters=50),
        ],
        PRODUCT_TYPE_THRESHOLD_CONFIGS=[],
    )

    client = app.test_client()
    response = client.get("/near-expiry")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "available_liters": 100,
            "batch_id": "milk-1",
            "expires_on": "2026-03-20",
            "product_type": "milk",
        }
    ]


def test_near_expiry_endpoint_applies_configured_threshold_per_product_type():
    app = create_app()
    app.config.update(
        TESTING=True,
        TODAY=date(2026, 3, 11),
        BATCHES=[
            Batch(batch_id="juice-1", product_type="juice", expires_on=date(2026, 3, 25), available_liters=100),
            Batch(batch_id="juice-2", product_type="juice", expires_on=date(2026, 4, 25), available_liters=100),
        ],
        PRODUCT_TYPE_THRESHOLD_CONFIGS=[
            ProductTypeThresholdConfig(product_type="juice", near_expiry_threshold_days=14)
        ],
    )

    client = app.test_client()
    response = client.get("/near-expiry")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "available_liters": 100,
            "batch_id": "juice-1",
            "expires_on": "2026-03-25",
            "product_type": "juice",
        }
    ]
