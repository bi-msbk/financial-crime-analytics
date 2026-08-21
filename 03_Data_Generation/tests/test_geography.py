from __future__ import annotations

import pandas as pd
import pytest

from generators.geography import (
    REQUIRED_COLUMNS,
    generate_geography,
)


def test_geography_returns_dataframe():
    df = generate_geography(count=20)

    assert isinstance(df, pd.DataFrame)


def test_geography_has_required_columns():
    df = generate_geography(count=20)

    assert list(df.columns) == REQUIRED_COLUMNS


def test_geography_has_expected_row_count():
    df = generate_geography(count=20)

    assert len(df) == 20


def test_geography_keys_are_unique():
    df = generate_geography(count=20)

    assert df["geography_key"].is_unique
    assert df["geography_id"].is_unique


def test_geography_identifiers_are_not_null():
    df = generate_geography(count=20)

    assert df["geography_key"].notna().all()
    assert df["geography_id"].notna().all()


def test_geography_is_uk_only():
    df = generate_geography(count=20)

    assert (df["country"] == "United Kingdom").all()


def test_geography_is_reproducible():
    first = generate_geography(count=20, seed=20260817)
    second = generate_geography(count=20, seed=20260817)

    pd.testing.assert_frame_equal(first, second)


def test_invalid_count_is_rejected():
    with pytest.raises(ValueError):
        generate_geography(count=0)
