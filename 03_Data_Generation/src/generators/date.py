from __future__ import annotations

# from datetime import date

import pandas as pd


REQUIRED_COLUMNS = [
    "date_key",
    "date",
    "year",
    "quarter",
    "month",
    "week",
    "day_of_week",
    "is_weekend",
    "is_month_end",
]


def generate_date(
    start_date: str = "2024-01-01",
    end_date: str = "2025-12-31",
) -> pd.DataFrame:
    """
    Generate the analytical date dimension.

    Grain:
        One row per calendar date.

    The generation is deterministic and does not use randomness.
    """

    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)

    if start > end:
        raise ValueError("start_date must be earlier than or equal to end_date")

    dates = pd.date_range(
        start=start,
        end=end,
        freq="D",
    )

    df = pd.DataFrame({"date": dates})

    df["date_key"] = (
        df["date"].dt.strftime("%Y%m%d").astype(int)
    )

    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.quarter
    df["month"] = df["date"].dt.month
    df["week"] = df["date"].dt.isocalendar().week.astype(int)

    # ISO weekday:
    # Monday = 1 ... Sunday = 7
    df["day_of_week"] = df["date"].dt.isocalendar().day.astype(int)

    df["is_weekend"] = df["day_of_week"].isin([6, 7])

    df["is_month_end"] = df["date"].dt.is_month_end

    return df[REQUIRED_COLUMNS].reset_index(drop=True)
