from __future__ import annotations

import numpy as np
import pandas as pd


ACCOUNT_TYPES = [
    "Current",
    "Savings",
    "Credit",
]

ACCOUNT_STATUSES = [
    "Active",
    "Closed",
    "Dormant",
]


def generate_accounts(
    customers: pd.DataFrame,
    count: int,
    seed: int,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """
    Generate synthetic banking accounts.

    Grain:
        One row per account.

    Accounts are assigned to existing customers. No customer identifiers
    are invented independently of the supplied customer dimension.
    """

    if count <= 0:
        raise ValueError("count must be greater than zero")

    if customers is None or customers.empty:
        raise ValueError("customers must contain at least one customer")

    required_customer_columns = {
        "customer_key",
        "customer_id",
        "customer_region",
        "customer_onboarding_date",
    }

    missing = required_customer_columns - set(customers.columns)

    if missing:
        raise ValueError(
            f"customers is missing required columns: {sorted(missing)}"
        )

    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)

    if start > end:
        raise ValueError("start_date must be before or equal to end_date")

    customer_data = customers.reset_index(drop=True).copy()

    customer_data["customer_onboarding_date"] = pd.to_datetime(
        customer_data["customer_onboarding_date"]
    )

    rng = np.random.default_rng(seed)

    # Select customers with replacement so a customer may own multiple accounts.
    selected_indices = rng.integers(
        low=0,
        high=len(customer_data),
        size=count,
    )

    selected_customers = customer_data.iloc[selected_indices].reset_index(
        drop=True
    )

    # Account opening dates cannot precede customer onboarding.
    account_open_dates = []

    for onboarding_date in selected_customers["customer_onboarding_date"]:
        earliest = max(start, onboarding_date)

        if earliest > end:
            raise ValueError(
                "At least one selected customer cannot have an account "
                "opened within the requested date range."
            )

        days_available = (end - earliest).days

        offset = int(rng.integers(0, days_available + 1))

        account_open_dates.append(
            earliest + pd.Timedelta(days=offset)
        )

    result = pd.DataFrame(
        {
            "account_key": np.arange(1, count + 1, dtype=np.int64),
            "account_id": [
                f"ACC{i:06d}" for i in range(1, count + 1)
            ],
            "customer_key": selected_customers["customer_key"].to_numpy(),
            "customer_id": selected_customers["customer_id"].to_numpy(),
            "account_type": rng.choice(
                ACCOUNT_TYPES,
                size=count,
            ),
            "account_status": rng.choice(
                ACCOUNT_STATUSES,
                size=count,
                p=[0.90, 0.05, 0.05],
            ),
            "account_open_date": pd.to_datetime(account_open_dates),
            "account_region": selected_customers[
                "customer_region"
            ].to_numpy(),
        }
    )

    return result
