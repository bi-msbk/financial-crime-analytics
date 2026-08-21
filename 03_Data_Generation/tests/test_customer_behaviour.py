from __future__ import annotations

import pandas as pd
import pytest

from src.behaviour.customer_behaviour import (
    REQUIRED_COLUMNS,
    TRANSACTION_CHANNELS,
    TRANSACTION_TYPES,
    MERCHANT_CATEGORIES,
    generate_customer_behaviour_profiles,
)

from src.generators.customer import generate_customer


CUSTOMER_COUNT = 500
SEED = 20260817


@pytest.fixture
def customers():
    return generate_customer(
        count=CUSTOMER_COUNT,
        seed=SEED,
        start_date="2024-01-01",
        end_date="2025-12-31",
    )


def test_behaviour_returns_dataframe(customers):
    df = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    assert isinstance(df, pd.DataFrame)


def test_behaviour_has_required_columns(customers):
    df = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    assert list(df.columns) == REQUIRED_COLUMNS


def test_behaviour_has_one_row_per_customer(customers):
    df = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    assert len(df) == len(customers)


def test_customer_keys_are_unique(customers):
    df = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    assert df["customer_key"].is_unique


def test_customer_ids_are_unique(customers):
    df = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    assert df["customer_id"].is_unique


def test_customer_keys_match_input(customers):
    df = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    assert set(df["customer_key"]) == set(customers["customer_key"])


def test_customer_ids_match_input(customers):
    df = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    assert set(df["customer_id"]) == set(customers["customer_id"])


def test_frequency_is_positive(customers):
    df = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    assert (df["expected_transaction_frequency"] > 0).all()


def test_typical_amount_is_positive(customers):
    df = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    assert (df["typical_transaction_amount"] > 0).all()


def test_channels_are_valid(customers):
    df = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    assert set(df["preferred_transaction_channel"]).issubset(
        set(TRANSACTION_CHANNELS)
    )


def test_transaction_types_are_valid(customers):
    df = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    assert set(df["preferred_transaction_type"]).issubset(
        set(TRANSACTION_TYPES)
    )


def test_merchant_categories_are_valid(customers):
    df = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    assert set(df["preferred_merchant_category"]).issubset(
        set(MERCHANT_CATEGORIES)
    )


def test_geography_is_populated(customers):
    df = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    assert df["normal_region"].notna().all()


def test_device_usage_is_positive(customers):
    df = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    assert (df["normal_device_count"] >= 1).all()


def test_typical_transaction_hour_is_valid(customers):
    df = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    assert df["typical_transaction_hour"].between(0, 23).all()


def test_behaviour_generation_is_reproducible(customers):
    df1 = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    df2 = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    pd.testing.assert_frame_equal(df1, df2)


def test_different_seed_changes_behaviour(customers):
    df1 = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    df2 = generate_customer_behaviour_profiles(
        customers,
        seed=SEED + 1,
    )

    assert not df1.equals(df2)


def test_empty_customers_are_rejected():
    customers = pd.DataFrame()

    with pytest.raises(ValueError):
        generate_customer_behaviour_profiles(
            customers,
            seed=SEED,
        )


def test_missing_customer_key_is_rejected():
    customers = pd.DataFrame(
        {
            "customer_id": ["CUST000001"],
        }
    )

    with pytest.raises(ValueError):
        generate_customer_behaviour_profiles(
            customers,
            seed=SEED,
        )


def test_missing_customer_id_is_rejected():
    customers = pd.DataFrame(
        {
            "customer_key": [1],
        }
    )

    with pytest.raises(ValueError):
        generate_customer_behaviour_profiles(
            customers,
            seed=SEED,
        )
