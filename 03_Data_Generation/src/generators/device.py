
from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "device_key",
    "device_id",
    "device_type",
    "operating_system",
    "device_first_seen_date",
    "device_region",
]


DEVICE_TYPES = [
    "Mobile",
    "Desktop",
    "Tablet",
]


OPERATING_SYSTEMS = [
    "iOS",
    "Android",
    "Windows",
    "macOS",
]


UK_REGIONS = [
    "London",
    "South East",
    "South West",
    "East of England",
    "West Midlands",
    "East Midlands",
    "Yorkshire and the Humber",
    "North West",
    "North East",
    "Wales",
    "Scotland",
    "Northern Ireland",
]


def generate_devices(
    count: int = 750,
    seed: int = 20260817,
    start_date: str = "2024-01-01",
    end_date: str = "2025-12-31",
) -> pd.DataFrame:
    """
    Generate a deterministic synthetic device dimension.

    Grain:
        One row per device.

    No real device identifiers or customer information are generated.
    """

    if count <= 0:
        raise ValueError("count must be greater than zero")

    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)

    if start > end:
        raise ValueError(
            "start_date must be earlier than or equal to end_date"
        )

    rng = np.random.default_rng(seed)

    device_key = np.arange(
        1,
        count + 1,
        dtype=np.int64,
    )

    device_id = [
        f"DEV{i:07d}"
        for i in device_key
    ]

    device_type = rng.choice(
        DEVICE_TYPES,
        size=count,
        p=[0.60, 0.25, 0.15],
    )

    operating_system = rng.choice(
        OPERATING_SYSTEMS,
        size=count,
        p=[0.35, 0.40, 0.15, 0.10],
    )

    device_region = rng.choice(
        UK_REGIONS,
        size=count,
        p=[
            0.18,
            0.14,
            0.08,
            0.08,
            0.08,
            0.06,
            0.08,
            0.10,
            0.05,
            0.05,
            0.08,
            0.02,
        ],
    )

    date_range_days = (end - start).days

    first_seen_offsets = rng.integers(
        0,
        date_range_days + 1,
        size=count,
    )

    device_first_seen_dates = (
        start
        + pd.to_timedelta(first_seen_offsets, unit="D")
    )

    return pd.DataFrame(
        {
            "device_key": device_key,
            "device_id": device_id,
            "device_type": device_type,
            "operating_system": operating_system,
            "device_first_seen_date": device_first_seen_dates,
            "device_region": device_region,
        }
    )
