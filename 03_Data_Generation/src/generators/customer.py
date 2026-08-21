from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "customer_key",
    "customer_id",
    "customer_segment",
    "customer_age_band",
    "customer_region",
    "customer_status",
    "customer_onboarding_date",
]

CUSTOMER_SEGMENTS = [
    "Mass Retail",
    "Affluent",
    "Premier",
]

AGE_BANDS = [
    "18-24",
    "25-34",
    "35-44",
    "45-54",
    "55-64",
    "65+",
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

CUSTOMER_STATUSES = [
    "Active",
    "Dormant",
    "Closed",
]


def generate_customer(
    count: int = 500,
    seed: int = 20260817,
    start_date: str = "2024-01-01",
    end_date: str = "2025-12-31",
) -> pd.DataFrame:
    """
    Generate a deterministic synthetic customer dimension.

    Grain:
        One row per customer.

    No real customer PII is generated.
    """

    if count <= 0:
        raise ValueError("count must be greater than zero")

    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)

    if start > end:
        raise ValueError("start_date must be earlier than or equal to end_date")

    rng = np.random.default_rng(seed)

    customer_key = np.arange(
        1,
        count + 1,
        dtype=np.int64,
    )

    customer_id = [
        f"CUST{i:06d}"
        for i in customer_key
    ]

    customer_segment = rng.choice(
        CUSTOMER_SEGMENTS,
        size=count,
        p=[0.75, 0.20, 0.05],
    )

    customer_age_band = rng.choice(
        AGE_BANDS,
        size=count,
        p=[0.08, 0.20, 0.25, 0.20, 0.17, 0.10],
    )

    customer_region = rng.choice(
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

    customer_status = rng.choice(
        CUSTOMER_STATUSES,
        size=count,
        p=[0.94, 0.04, 0.02],
    )

    date_range_days = (end - start).days

    onboarding_offsets = rng.integers(
        0,
        date_range_days + 1,
        size=count,
    )

    onboarding_dates = (
        start
        + pd.to_timedelta(onboarding_offsets, unit="D")
    )

    return pd.DataFrame(
        {
            "customer_key": customer_key,
            "customer_id": customer_id,
            "customer_segment": customer_segment,
            "customer_age_band": customer_age_band,
            "customer_region": customer_region,
            "customer_status": customer_status,
            "customer_onboarding_date": onboarding_dates,
        }
    )

def generate_customers(
    count: int = 500,
    seed: int = 20260817,
    start_date: str = "2024-01-01",
    end_date: str = "2025-12-31",
) -> pd.DataFrame:
    """
    Compatibility wrapper for downstream generators.

    The canonical customer generator remains generate_customer().
    """
    return generate_customer(
        count=count,
        seed=seed,
        start_date=start_date,
        end_date=end_date,
    )
