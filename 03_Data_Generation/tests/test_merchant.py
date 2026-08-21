from __future__ import annotations

import pandas as pd
import pytest

from src.generators.merchant import (
    MERCHANT_CATEGORIES,
    MERCHANT_STATUSES,
    generate_merchants,
)


SEED = 20260817
MERCHANT_COUNT = 500
START_DATE = "2024-01-01"
END_DATE = "2025-12-31"


def test_merchant_returns_dataframe():
    df = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    assert isinstance(df, pd.DataFrame)


def test_merchant_has_required_columns():
    df = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    required = {
        "merchant_key",
        "merchant_id",
        "merchant_name",
        "merchant_category",
        "merchant_region",
        "merchant_country",
        "merchant_status",
    }

    assert required.issubset(df.columns)


def test_merchant_has_expected_row_count():
    df = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    assert len(df) == MERCHANT_COUNT


def test_merchant_keys_are_unique():
    df = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    assert df["merchant_key"].is_unique


def test_merchant_identifiers_are_unique():
    df = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    assert df["merchant_id"].is_unique


def test_merchant_identifiers_are_not_null():
    df = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    assert df["merchant_key"].notna().all()
    assert df["merchant_id"].notna().all()
    assert df["merchant_name"].notna().all()


def test_merchant_identifier_format():
    df = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    assert df["merchant_id"].str.match(r"^MER\d{6}$").all()


def test_merchant_categories_are_valid():
    df = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    assert df["merchant_category"].isin(
        MERCHANT_CATEGORIES
    ).all()


def test_merchant_statuses_are_valid():
    df = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    assert df["merchant_status"].isin(
        MERCHANT_STATUSES
    ).all()


def test_merchant_country_is_uk():
    df = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    assert (df["merchant_country"] == "United Kingdom").all()


def test_merchant_regions_are_valid():
    df = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    assert df["merchant_region"].notna().all()


def test_merchant_keys_are_sequential():
    df = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    expected = list(range(1, MERCHANT_COUNT + 1))

    assert df["merchant_key"].tolist() == expected


def test_merchant_generation_is_reproducible():
    first = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    second = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    pd.testing.assert_frame_equal(first, second)


def test_different_seed_changes_generated_attributes():
    first = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    second = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED + 1,
    )

    assert not first.equals(second)


def test_invalid_count_is_rejected():
    with pytest.raises(ValueError):
        generate_merchants(
            count=0,
            seed=SEED,
        )
