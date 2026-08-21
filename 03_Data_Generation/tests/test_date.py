from __future__ import annotations

import pandas as pd
import pytest

from generators.date import (
    REQUIRED_COLUMNS,
    generate_date,
)


START_DATE = "2024-01-01"
END_DATE = "2025-12-31"


def test_date_returns_dataframe():
    df = generate_date(START_DATE, END_DATE)

    assert isinstance(df, pd.DataFrame)


def test_date_has_required_columns():
    df = generate_date(START_DATE, END_DATE)

    assert list(df.columns) == REQUIRED_COLUMNS


def test_date_has_expected_row_count():
    df = generate_date(START_DATE, END_DATE)

    # 2024 is a leap year.
    assert len(df) == 731


def test_date_key_is_unique():
    df = generate_date(START_DATE, END_DATE)

    assert df["date_key"].is_unique


def test_date_is_unique():
    df = generate_date(START_DATE, END_DATE)

    assert df["date"].is_unique


def test_date_has_no_null_values():
    df = generate_date(START_DATE, END_DATE)

    assert df["date"].notna().all()
    assert df["date_key"].notna().all()


def test_date_sequence_has_no_gaps():
    df = generate_date(START_DATE, END_DATE)

    expected = pd.date_range(
        START_DATE,
        END_DATE,
        freq="D",
    )

    pd.testing.assert_series_equal(
        df["date"],
        pd.Series(expected, name="date"),
        check_index=False,
    )


def test_date_attributes_are_correct():
    df = generate_date(START_DATE, END_DATE)

    first = df.iloc[0]

    assert first["date"] == pd.Timestamp("2024-01-01")
    assert first["date_key"] == 20240101
    assert first["year"] == 2024
    assert first["quarter"] == 1
    assert first["month"] == 1
    assert first["day_of_week"] == 1
    assert bool(first["is_weekend"]) is False


def test_weekend_flag_is_correct():
    df = generate_date(START_DATE, END_DATE)

    saturday = df.loc[
        df["date"] == pd.Timestamp("2024-01-06")
    ].iloc[0]

    sunday = df.loc[
        df["date"] == pd.Timestamp("2024-01-07")
    ].iloc[0]

    monday = df.loc[
        df["date"] == pd.Timestamp("2024-01-08")
    ].iloc[0]

    assert bool(saturday["is_weekend"]) is True
    assert bool(sunday["is_weekend"]) is True
    assert bool(monday["is_weekend"]) is False


def test_month_end_flag_is_correct():
    df = generate_date(START_DATE, END_DATE)

    month_end = df.loc[
        df["date"] == pd.Timestamp("2024-01-31")
    ].iloc[0]

    next_day = df.loc[
        df["date"] == pd.Timestamp("2024-02-01")
    ].iloc[0]

    assert bool(month_end["is_month_end"]) is True
    assert bool(next_day["is_month_end"]) is False


def test_date_generation_is_reproducible():
    first = generate_date(START_DATE, END_DATE)
    second = generate_date(START_DATE, END_DATE)

    pd.testing.assert_frame_equal(first, second)


def test_invalid_date_range_is_rejected():
    with pytest.raises(ValueError):
        generate_date(
            start_date="2025-12-31",
            end_date="2024-01-01",
        )
