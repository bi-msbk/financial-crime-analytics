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
    "alert_id",
    "transaction_id",
    "rule_id",
    "alert_timestamp",
    "alert_status",
    "alert_outcome",
    "confirmed_fraud_flag",
]

RULES = [
    {
        "rule_id": "RULE001",
        "name": "High Transaction Amount",
        "category": "High Amount",
    },
    {
        "rule_id": "RULE002",
        "name": "High Transaction Velocity",
        "category": "Velocity",
    },
    {
        "rule_id": "RULE003",
        "name": "New Device",
        "category": "New Device",
    },
    {
        "rule_id": "RULE004",
        "name": "Geographic Anomaly",
        "category": "Geographic Anomaly",
    },
    {
        "rule_id": "RULE005",
        "name": "Unusual Transaction Timing",
        "category": "Timing",
    },
    {
        "rule_id": "RULE006",
        "name": "Suspicious Merchant Activity",
        "category": "Merchant Risk",
    },
    {
        "rule_id": "RULE007",
        "name": "Behavioural Deviation",
        "category": "Behavioural",
    },
]


def _validate_inputs(transactions: pd.DataFrame) -> None:
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

    if transactions["transaction_id"].isna().any():
        raise ValueError("transaction_id must not contain null values")

    if not transactions["transaction_id"].is_unique:
        raise ValueError("transaction_id must be unique")

    if transactions["transaction_amount"].isna().any():
        raise ValueError(
            "transaction_amount must not contain null values"
        )

    if (transactions["transaction_amount"] <= 0).any():
        raise ValueError(
            "transaction_amount must be greater than zero"
        )


def _rule_trigger_probability(
    rule_index: int,
    fraud_flag: bool,
    rng: np.random.Generator,
) -> bool:
    """
    Generate an imperfect control decision.

    Fraudulent transactions have a higher probability of detection,
    while legitimate transactions retain a small false-positive
    probability.
    """

    detection_rates = [
        0.72,
        0.68,
        0.70,
        0.64,
        0.60,
        0.58,
        0.66,
    ]

    false_positive_rates = [
        0.08,
        0.07,
        0.06,
        0.05,
        0.08,
        0.07,
        0.09,
    ]

    probability = (
        detection_rates[rule_index]
        if fraud_flag
        else false_positive_rates[rule_index]
    )

    return bool(rng.random() < probability)


def _candidate_rules(
    transaction: pd.Series,
) -> list[int]:
    """
    Determine which controls are applicable to a transaction.

    The rules intentionally overlap so that one transaction can
    generate multiple alerts.
    """

    candidates: list[int] = []

    amount = float(transaction["transaction_amount"])

    if amount >= 500:
        candidates.append(0)

    if amount >= 300:
        candidates.append(1)

    if "transaction_channel" in transaction.index:
        channel = str(transaction["transaction_channel"])

        if channel in {"Online", "Mobile"}:
            candidates.append(2)

    if "device_id" in transaction.index:
        device_id = str(transaction["device_id"])

        if device_id.endswith(("000", "001", "002")):
            candidates.append(2)

    if "geography_id" in transaction.index:
        geography_id = str(transaction["geography_id"])

        if geography_id.endswith(("0", "1")):
            candidates.append(3)

    if "transaction_timestamp" in transaction.index:
        timestamp = pd.Timestamp(
            transaction["transaction_timestamp"]
        )

        if timestamp.hour < 6 or timestamp.hour >= 23:
            candidates.append(4)

    if "merchant_id" in transaction.index:
        merchant_id = str(transaction["merchant_id"])

        if merchant_id.endswith(("000", "001", "002", "003")):
            candidates.append(5)

    if bool(transaction["fraud_flag"]):
        candidates.append(6)

    return sorted(set(candidates))


def evaluate_controls(
    transactions: pd.DataFrame,
    seed: int = 20260817,
) -> pd.DataFrame:
    """
    Evaluate synthetic fraud-monitoring controls.

    Grain:
        One row per generated fraud-monitoring alert.

    Relationship:
        One transaction may generate zero, one or multiple alerts.
    """

    _validate_inputs(transactions)

    rng = np.random.default_rng(seed)

    alerts: list[dict] = []

    alert_counter = 1

    for _, transaction in transactions.iterrows():

        fraud_flag = bool(transaction["fraud_flag"])

        candidates = _candidate_rules(transaction)

        for rule_index in candidates:

            if not _rule_trigger_probability(
                rule_index=rule_index,
                fraud_flag=fraud_flag,
                rng=rng,
            ):
                continue

            if (
                "transaction_timestamp" in transaction.index
                and pd.notna(transaction["transaction_timestamp"])
            ):
                alert_timestamp = pd.Timestamp(
                    transaction["transaction_timestamp"]
                )
            else:
                alert_timestamp = pd.Timestamp("2024-01-01")

            alert_outcome = (
                "True Positive"
                if fraud_flag
                else "False Positive"
            )

            alerts.append(
                {
                    "alert_id": f"ALERT{alert_counter:09d}",
                    "transaction_id": transaction["transaction_id"],
                    "rule_id": RULES[rule_index]["rule_id"],
                    "alert_timestamp": alert_timestamp,
                    "alert_status": "Generated",
                    "alert_outcome": alert_outcome,
                    "confirmed_fraud_flag": fraud_flag,
                }
            )

            alert_counter += 1

    if not alerts:
        return pd.DataFrame(
            columns=REQUIRED_COLUMNS
        )

    result = pd.DataFrame(alerts)

    result["confirmed_fraud_flag"] = (
        result["confirmed_fraud_flag"].astype(bool)
    )

    result["alert_timestamp"] = pd.to_datetime(
        result["alert_timestamp"]
    )

    return result[REQUIRED_COLUMNS]
