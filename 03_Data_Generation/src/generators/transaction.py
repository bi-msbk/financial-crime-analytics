
from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "transaction_key",
    "transaction_id",
    "customer_key",
    "account_key",
    "merchant_key",
    "device_key",
    "geography_key",
    "date_key",
    "transaction_timestamp",
    "transaction_amount",
    "currency",
    "transaction_type",
    "transaction_channel",
    "transaction_status",
]


TRANSACTION_TYPES = [
    "Card Purchase",
    "Cash Withdrawal",
    "Transfer",
    "Direct Debit",
]


TRANSACTION_CHANNELS = [
    "Online",
    "Mobile",
    "Card Present",
    "ATM",
    "Branch",
]


TRANSACTION_STATUSES = [
    "Completed",
    "Pending",
    "Declined",
]


def generate_transactions(
    customers: pd.DataFrame,
    accounts: pd.DataFrame,
    merchants: pd.DataFrame,
    devices: pd.DataFrame,
    geography: pd.DataFrame,
    dates: pd.DataFrame,
    count: int,
    seed: int,
    start_date: str,
    end_date: str,
    behaviour: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Generate a deterministic synthetic transaction fact table.

    Grain:
        One row per financial transaction.

    Fraud is deliberately NOT assigned here.
    Fraud scenarios are introduced by the dedicated fraud simulation layer.
    """

    if count <= 0:
        raise ValueError("count must be greater than zero")

    required_inputs = {
        "customers": [
            "customer_key",
            "customer_id",
        ],
        "accounts": [
            "account_key",
            "account_id",
            "customer_key",
            "customer_id",
            "account_open_date",
        ],
        "merchants": [
            "merchant_key",
            "merchant_id",
        ],
        "devices": [
            "device_key",
            "device_id",
        ],
        "geography": [
            "geography_key",
            "geography_id",
        ],
        "dates": [
            "date_key",
            "date",
        ],
    }

    supplied = {
        "customers": customers,
        "accounts": accounts,
        "merchants": merchants,
        "devices": devices,
        "geography": geography,
        "dates": dates,
    }

    for name, columns in required_inputs.items():
        dataframe = supplied[name]

        if dataframe is None or dataframe.empty:
            raise ValueError(f"{name} must contain data")

        missing = set(columns) - set(dataframe.columns)

        if missing:
            raise ValueError(
                f"{name} is missing required columns: "
                f"{sorted(missing)}"
            )

    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)

    if start > end:
        raise ValueError(
            "start_date must be before or equal to end_date"
        )

    rng = np.random.default_rng(seed)

    customer_data = customers.reset_index(drop=True)
    account_data = accounts.reset_index(drop=True)
    merchant_data = merchants.reset_index(drop=True)
    device_data = devices.reset_index(drop=True)
    geography_data = geography.reset_index(drop=True)
    date_data = dates.reset_index(drop=True).copy()

    date_data["date"] = pd.to_datetime(date_data["date"])

    valid_dates = date_data[
        date_data["date"].between(start, end)
    ].reset_index(drop=True)

    if valid_dates.empty:
        raise ValueError(
            "dates contains no dates within the requested range"
        )

    # Select accounts first so customer-account relationships remain valid.
    account_indices = rng.integers(
        0,
        len(account_data),
        size=count,
    )

    selected_accounts = account_data.iloc[
        account_indices
    ].reset_index(drop=True)

    # Select associated customers using the account relationship.
    customer_lookup = customer_data.set_index("customer_key")

    selected_customers = customer_lookup.loc[
        selected_accounts["customer_key"]
    ].reset_index()

    # Transaction dates must not precede account opening.
    transaction_dates = []

    for account_open_date in selected_accounts["account_open_date"]:
        earliest = max(
            start,
            pd.Timestamp(account_open_date),
        )

        if earliest > end:
            raise ValueError(
                "Selected account cannot have a transaction "
                "within the requested date range."
            )

        days_available = (end - earliest).days

        offset = int(
            rng.integers(
                0,
                days_available + 1,
            )
        )

        transaction_dates.append(
            earliest + pd.Timedelta(days=offset)
        )

    transaction_dates = pd.to_datetime(transaction_dates)

    # Choose a valid geography, merchant and device for each transaction.
    merchant_indices = rng.integers(
        0,
        len(merchant_data),
        size=count,
    )

    device_indices = rng.integers(
        0,
        len(device_data),
        size=count,
    )

    geography_indices = rng.integers(
        0,
        len(geography_data),
        size=count,
    )

    selected_merchants = merchant_data.iloc[
        merchant_indices
    ].reset_index(drop=True)

    selected_devices = device_data.iloc[
        device_indices
    ].reset_index(drop=True)

    selected_geographies = geography_data.iloc[
        geography_indices
    ].reset_index(drop=True)

    # Generate realistic positive transaction amounts.
    amounts = rng.lognormal(
        mean=np.log(55),
        sigma=1.0,
        size=count,
    )

    amounts = np.clip(
        amounts,
        1.00,
        10000.00,
    ).round(2)

    # Generate time-of-day variation.
    hours = rng.choice(
    np.arange(24),
    size=count,
    p=np.array([
        0.01, 0.005, 0.005, 0.005,
        0.01, 0.015, 0.025, 0.04,
        0.06, 0.07, 0.07, 0.065,
        0.06, 0.06, 0.06, 0.065,
        0.07, 0.08, 0.08, 0.07,
        0.06, 0.045, 0.025, 0.015,
    ]) / np.sum([
        0.01, 0.005, 0.005, 0.005,
        0.01, 0.015, 0.025, 0.04,
        0.06, 0.07, 0.07, 0.065,
        0.06, 0.06, 0.06, 0.065,
        0.07, 0.08, 0.08, 0.07,
        0.06, 0.045, 0.025, 0.015,
    ]),
)

    minutes = rng.integers(
        0,
        60,
        size=count,
    )

    seconds = rng.integers(
        0,
        60,
        size=count,
    )

    timestamps = (
        transaction_dates
        + pd.to_timedelta(hours, unit="h")
        + pd.to_timedelta(minutes, unit="m")
        + pd.to_timedelta(seconds, unit="s")
    )

    result = pd.DataFrame(
        {
            "transaction_key": np.arange(
                1,
                count + 1,
                dtype=np.int64,
            ),
            "transaction_id": [
                f"TXN{i:08d}"
                for i in range(1, count + 1)
            ],
            "customer_key": selected_customers[
                "customer_key"
            ].to_numpy(),
            "account_key": selected_accounts[
                "account_key"
            ].to_numpy(),
            "merchant_key": selected_merchants[
                "merchant_key"
            ].to_numpy(),
            "device_key": selected_devices[
                "device_key"
            ].to_numpy(),
            "geography_key": selected_geographies[
                "geography_key"
            ].to_numpy(),
            "date_key": timestamps.strftime("%Y%m%d").astype(int),
            "transaction_timestamp": timestamps,
            "transaction_amount": amounts,
            "currency": "GBP",
            "transaction_type": rng.choice(
                TRANSACTION_TYPES,
                size=count,
                p=[0.60, 0.10, 0.20, 0.10],
            ),
            "transaction_channel": rng.choice(
                TRANSACTION_CHANNELS,
                size=count,
                p=[0.30, 0.25, 0.30, 0.10, 0.05],
            ),
            "transaction_status": rng.choice(
                TRANSACTION_STATUSES,
                size=count,
                p=[0.94, 0.03, 0.03],
            ),
        }
    )

    # Ensure date_key exists in the supplied date dimension.
    valid_date_keys = set(
        valid_dates["date_key"].astype(int)
    )

    if not result["date_key"].isin(valid_date_keys).all():
        raise ValueError(
            "Generated transaction date_key does not exist "
            "in the supplied date dimension."
        )

    return result
