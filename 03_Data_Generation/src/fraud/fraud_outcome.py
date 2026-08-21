from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_TRANSACTION_COLUMNS = [
    "transaction_id",
    "transaction_amount",
    "fraud_flag",
    "fraud_type",
    "fraud_loss_amount",
]

REQUIRED_COLUMNS = [
    "fraud_outcome_key",
    "fraud_outcome_id",
    "transaction_key",
    "transaction_id",
    "fraud_type",
    "fraud_confirmed_date",
    "fraud_loss_amount",
    "fraud_outcome_source",
]

FRAUD_TYPES = [
    "Account Takeover",
    "High Value",
    "High Velocity",
    "New Device",
    "Geographic Anomaly",
    "Online Fraud",
    "Merchant Risk",
    "Behavioural Deviation",
]

FRAUD_OUTCOME_SOURCES = [
    "Synthetic Fraud Simulation",
]


def generate_fraud_outcomes(
    transactions: pd.DataFrame,
    seed: int = 20260817,
) -> pd.DataFrame:
    """
    Materialise confirmed fraud outcomes from the fraud-simulated
    transaction population.

    Grain:
        One row per confirmed fraud outcome.

    Relationship:
        One transaction may have zero or one fraud outcome.
    """

    if transactions is None or transactions.empty:
        raise ValueError("transactions must not be empty")

    missing = [
        column
        for column in REQUIRED_TRANSACTION_COLUMNS
        if column not in transactions.columns
    ]

    if missing:
        raise ValueError(
            f"transactions is missing required columns: {missing}"
        )

    if transactions["transaction_id"].duplicated().any():
        raise ValueError("transaction_id must be unique")

    fraud_transactions = transactions[
        transactions["fraud_flag"].astype(bool)
    ].copy()

    if fraud_transactions.empty:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    rng = np.random.default_rng(seed)

    fraud_transactions = fraud_transactions.sort_values(
        "transaction_id"
    ).reset_index(drop=True)

    outcome_count = len(fraud_transactions)

    fraud_types = []

    fraud_types = fraud_transactions["fraud_type"].map(
    {
        "account_takeover": "Account Takeover",
        "high_value": "High Value",
        "high_velocity": "High Velocity",
        "new_device": "New Device",
        "geographic_anomaly": "Geographic Anomaly",
        "online_fraud": "Online Fraud",
        "merchant_risk": "Merchant Risk",
        "behavioural_deviation": "Behavioural Deviation",
    }
    ).tolist()

    if "transaction_timestamp" in fraud_transactions.columns:
        confirmed_dates = (
        pd.to_datetime(
            fraud_transactions["transaction_timestamp"]
        )
        .dt.normalize()
    )
    else:
        confirmed_dates = pd.Series(
        pd.Timestamp("2024-01-01"),
        index=fraud_transactions.index,
    )

    outcome = pd.DataFrame(
        {
            "fraud_outcome_key": np.arange(
                1,
                outcome_count + 1,
                dtype=np.int64,
            ),
            "fraud_outcome_id": [
                f"FOUT{i:08d}"
                for i in range(1, outcome_count + 1)
            ],
            "transaction_key": np.arange(
                1,
                outcome_count + 1,
                dtype=np.int64,
            ),
            "transaction_id": fraud_transactions[
                "transaction_id"
            ].to_numpy(),
            "fraud_type": fraud_types,
            "fraud_confirmed_date": confirmed_dates.to_numpy(),
            "fraud_loss_amount": fraud_transactions[
                "fraud_loss_amount"
            ].astype(float).to_numpy(),
            "fraud_outcome_source": [
                "Synthetic Fraud Simulation"
            ] * outcome_count,
        }
    )

    return outcome[REQUIRED_COLUMNS]
