from __future__ import annotations

import pandas as pd
import pytest

from generators.customer import (
    AGE_BANDS,
    CUSTOMER_SEGMENTS,
    CUSTOMER_STATUSES,
    REQUIRED_COLUMNS,
    UK_REGIONS,
    generate_customer,
)


START_DATE = "2024-01-01"
END_DATE = "2025-12-31"


def test_customer_returns_dataframe():
    df = generate_customer(count=500)

    assert isinstance(df, pd.DataFrame)


def test_customer_has_required_columns():
    df = generate_customer(count=500)

    assert list(df.columns) == REQUIRED_COLUMNS


def test_customer_has_expected_row_count():
    df = generate_customer(count=500)

    assert len(df) == 500


def test_customer_keys_are_unique():
    df = generate_customer(count=500)

    assert df["customer_key"].is_unique
    assert df["customer_id"].is_unique


def test_customer_identifiers_are_not_null():
    df = generate_customer(count=500)

    assert df["customer_key"].notna().all()
    assert df["customer_id"].notna().all()


def test_customer_identifier_format():
    df = generate_customer(count=500)

    assert df["customer_id"].str.match(r"^CUST\d{6}$").all()


def test_customer_domains_are_valid():
    df = generate_customer(count=500)

    assert set(df["customer_segment"]).issubset(CUSTOMER_SEGMENTS)
    assert set(df["customer_age_band"]).issubset(AGE_BANDS)
    assert set(df["customer_region"]).issubset(UK_REGIONS)
    assert set(df["customer_status"]).issubset(CUSTOMER_STATUSES)


def test_customer_onboarding_dates_are_valid():
    df = generate_customer(
        count=500,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    assert df["customer_onboarding_date"].notna().all()

    assert (
        df["customer_onboarding_date"]
        >= pd.Timestamp(START_DATE)
    ).all()

    assert (
        df["customer_onboarding_date"]
        <= pd.Timestamp(END_DATE)
    ).all()


def test_customer_keys_are_sequential():
    df = generate_customer(count=500)

    expected = list(range(1, 501))

    assert df["customer_key"].tolist() == expected


def test_customer_generation_is_reproducible():
    first = generate_customer(
        count=500,
        seed=20260817,
    )

    second = generate_customer(
        count=500,
        seed=20260817,
    )

    pd.testing.assert_frame_equal(first, second)


def test_different_seed_changes_generated_attributes():
    first = generate_customer(
        count=500,
        seed=20260817,
    )

    second = generate_customer(
        count=500,
        seed=20260818,
    )

    assert not first.equals(second)


def test_invalid_count_is_rejected():
    with pytest.raises(ValueError):
        generate_customer(count=0)


def test_invalid_date_range_is_rejected():
    with pytest.raises(ValueError):
        generate_customer(
            count=500,
            start_date="2025-12-31",
            end_date="2024-01-01",
        )
