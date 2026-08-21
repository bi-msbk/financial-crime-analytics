from __future__ import annotations

import numpy as np
import pandas as pd


MERCHANT_CATEGORIES = [
    "Retail",
    "Groceries",
    "Travel",
    "Hospitality",
    "Utilities",
    "Digital Services",
    "Entertainment",
]


MERCHANT_STATUSES = [
    "Active",
    "Inactive",
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


MERCHANT_PREFIXES = [
    "North",
    "Central",
    "Premier",
    "United",
    "Metro",
    "National",
    "Royal",
    "City",
    "Crown",
    "Green",
]


MERCHANT_SUFFIXES = [
    "Retail",
    "Stores",
    "Market",
    "Services",
    "Trading",
    "Group",
    "Direct",
    "Online",
    "Partners",
    "Limited",
]


def generate_merchants(
    count: int = 500,
    seed: int = 20260817,
) -> pd.DataFrame:
    """
    Generate a deterministic synthetic merchant dimension.

    Grain:
        One row per merchant.

    No real merchant information is generated.
    """

    if count <= 0:
        raise ValueError("count must be greater than zero")

    rng = np.random.default_rng(seed)

    merchant_key = np.arange(
        1,
        count + 1,
        dtype=np.int64,
    )

    merchant_id = [
        f"MER{i:06d}"
        for i in merchant_key
    ]

    merchant_names = [
        f"{rng.choice(MERCHANT_PREFIXES)} "
        f"{rng.choice(MERCHANT_SUFFIXES)} "
        f"{i:04d}"
        for i in merchant_key
    ]

    merchant_category = rng.choice(
        MERCHANT_CATEGORIES,
        size=count,
        p=[
            0.25,
            0.20,
            0.10,
            0.10,
            0.10,
            0.10,
            0.15,
        ],
    )

    merchant_region = rng.choice(
        UK_REGIONS,
        size=count,
    )

    merchant_status = rng.choice(
        MERCHANT_STATUSES,
        size=count,
        p=[0.95, 0.05],
    )

    return pd.DataFrame(
        {
            "merchant_key": merchant_key,
            "merchant_id": merchant_id,
            "merchant_name": merchant_names,
            "merchant_category": merchant_category,
            "merchant_region": merchant_region,
            "merchant_country": "United Kingdom",
            "merchant_status": merchant_status,
        }
    )
