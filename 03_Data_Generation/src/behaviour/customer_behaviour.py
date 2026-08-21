from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_CUSTOMER_COLUMNS = [
    "customer_key",
    "customer_id",
]

REQUIRED_COLUMNS = [
    "customer_key",
    "customer_id",
    "expected_transaction_frequency",
    "typical_transaction_amount",
    "preferred_transaction_channel",
    "preferred_transaction_type",
    "preferred_merchant_category",
    "normal_region",
    "normal_device_count",
    "typical_transaction_hour",
]


TRANSACTION_CHANNELS = [
    "Online",
    "Mobile",
    "Card Present",
    "ATM",
    "Branch",
]


TRANSACTION_TYPES = [
    "Purchase",
    "Cash Withdrawal",
    "Transfer",
    "Direct Debit",
    "Payment",
]


MERCHANT_CATEGORIES = [
    "Retail",
    "Groceries",
    "Travel",
    "Hospitality",
    "Utilities",
    "Digital Services",
    "Entertainment",
]


def generate_customer_behaviour_profiles(
    customers: pd.DataFrame,
    seed: int = 20260817,
) -> pd.DataFrame:
    """
    Generate one behavioural baseline profile per customer.

    Grain:
        One row per customer.

    The profiles represent normal synthetic customer behaviour and are
    subsequently used by transaction and fraud simulation logic.
    """

    if customers is None or customers.empty:
        raise ValueError("customers must contain at least one row")

    missing_columns = [
        column
        for column in REQUIRED_CUSTOMER_COLUMNS
        if column not in customers.columns
    ]

    if missing_columns:
        raise ValueError(
            f"customers is missing required columns: {missing_columns}"
        )

    if customers["customer_key"].isna().any():
        raise ValueError("customer_key must not contain null values")

    if customers["customer_id"].isna().any():
        raise ValueError("customer_id must not contain null values")

    if not customers["customer_key"].is_unique:
        raise ValueError("customer_key must be unique")

    if not customers["customer_id"].is_unique:
        raise ValueError("customer_id must be unique")

    rng = np.random.default_rng(seed)

    count = len(customers)

    # Customer transaction frequency:
    # most customers are typical-frequency users, with realistic variation.
    expected_transaction_frequency = np.maximum(
        1,
        rng.lognormal(
            mean=np.log(8.0),
            sigma=0.65,
            size=count,
        ).round().astype(np.int64),
    )

    # Typical transaction value.
    typical_transaction_amount = np.round(
        np.maximum(
            5.0,
            rng.lognormal(
                mean=np.log(45.0),
                sigma=0.65,
                size=count,
            ),
        ),
        2,
    )

    preferred_transaction_channel = rng.choice(
        TRANSACTION_CHANNELS,
        size=count,
        p=[
            0.30,
            0.35,
            0.25,
            0.07,
            0.03,
        ],
    )

    preferred_transaction_type = rng.choice(
        TRANSACTION_TYPES,
        size=count,
        p=[
            0.55,
            0.08,
            0.15,
            0.12,
            0.10,
        ],
    )

    preferred_merchant_category = rng.choice(
        MERCHANT_CATEGORIES,
        size=count,
        p=[
            0.22,
            0.20,
            0.10,
            0.12,
            0.12,
            0.14,
            0.10,
        ],
    )

    # Use the customer's existing region as the normal geographic baseline.
    if "customer_region" in customers.columns:
        normal_region = customers["customer_region"].to_numpy(copy=True)
    else:
        raise ValueError(
            "customers must contain customer_region for behavioural geography"
        )

    # Normal device usage: most customers use a small number of devices.
    normal_device_count = np.maximum(
        1,
        rng.poisson(
            lam=1.8,
            size=count,
        ) + 1,
    )

    # Typical transaction hour with stronger daytime/evening activity.
    hour_weights = np.array(
        [
            0.010,
            0.005,
            0.005,
            0.005,
            0.010,
            0.015,
            0.025,
            0.040,
            0.060,
            0.070,
            0.070,
            0.065,
            0.060,
            0.060,
            0.060,
            0.065,
            0.070,
            0.080,
            0.080,
            0.070,
            0.060,
            0.045,
            0.025,
            0.015,
        ],
        dtype=float,
    )

    hour_weights = hour_weights / hour_weights.sum()

    typical_transaction_hour = rng.choice(
        np.arange(24),
        size=count,
        p=hour_weights,
    )

    return pd.DataFrame(
        {
            "customer_key": customers["customer_key"].to_numpy(copy=True),
            "customer_id": customers["customer_id"].to_numpy(copy=True),
            "expected_transaction_frequency":
                expected_transaction_frequency,
            "typical_transaction_amount":
                typical_transaction_amount,
            "preferred_transaction_channel":
                preferred_transaction_channel,
            "preferred_transaction_type":
                preferred_transaction_type,
            "preferred_merchant_category":
                preferred_merchant_category,
            "normal_region":
                normal_region,
            "normal_device_count":
                normal_device_count,
            "typical_transaction_hour":
                typical_transaction_hour,
        }
    )[REQUIRED_COLUMNS]
