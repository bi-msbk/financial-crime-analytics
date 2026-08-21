
from __future__ import annotations

import pandas as pd
import pytest

from src.generators.device import (
    DEVICE_TYPES,
    OPERATING_SYSTEMS,
    REQUIRED_COLUMNS,
    UK_REGIONS,
    generate_devices,
)


START_DATE = "2024-01-01"
END_DATE = "2025-12-31"


def test_device_returns_dataframe():
    df = generate_devices(count=750)

    assert isinstance(df, pd.DataFrame)


def test_device_has_required_columns():
    df = generate_devices(count=750)

    assert list(df.columns) == REQUIRED_COLUMNS


def test_device_has_expected_row_count():
    df = generate_devices(count=750)

    assert len(df) == 750


def test_device_keys_are_unique():
    df = generate_devices(count=750)

    assert df["device_key"].is_unique


def test_device_identifiers_are_unique():
    df = generate_devices(count=750)

    assert df["device_id"].is_unique


def test_device_identifiers_are_not_null():
    df = generate_devices(count=750)

    assert df["device_id"].notna().all()
    assert df["device_key"].notna().all()


def test_device_identifier_format():
    df = generate_devices(count=750)

    assert df["device_id"].str.match(r"^DEV\d{7}$").all()


def test_device_keys_are_sequential():
    df = generate_devices(count=750)

    expected = list(range(1, 751))

    assert df["device_key"].tolist() == expected


def test_device_types_are_valid():
    df = generate_devices(count=750)

    assert set(df["device_type"]).issubset(
        set(DEVICE_TYPES)
    )


def test_device_operating_systems_are_valid():
    df = generate_devices(count=750)

    assert set(df["operating_system"]).issubset(
        set(OPERATING_SYSTEMS)
    )


def test_device_regions_are_valid():
    df = generate_devices(count=750)

    assert set(df["device_region"]).issubset(
        set(UK_REGIONS)
    )


def test_device_first_seen_dates_are_valid():
    df = generate_devices(
        count=750,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    assert (
        df["device_first_seen_date"]
        >= pd.Timestamp(START_DATE)
    ).all()

    assert (
        df["device_first_seen_date"]
        <= pd.Timestamp(END_DATE)
    ).all()


def test_device_generation_is_reproducible():
    df1 = generate_devices(
        count=750,
        seed=20260817,
    )

    df2 = generate_devices(
        count=750,
        seed=20260817,
    )

    pd.testing.assert_frame_equal(df1, df2)


def test_different_seed_changes_generated_attributes():
    df1 = generate_devices(
        count=750,
        seed=20260817,
    )

    df2 = generate_devices(
        count=750,
        seed=20260818,
    )

    assert not df1.equals(df2)


def test_invalid_count_is_rejected():
    with pytest.raises(ValueError):
        generate_devices(count=0)


def test_invalid_date_range_is_rejected():
    with pytest.raises(ValueError):
        generate_devices(
            count=750,
            start_date="2025-12-31",
            end_date="2024-01-01",
        )
