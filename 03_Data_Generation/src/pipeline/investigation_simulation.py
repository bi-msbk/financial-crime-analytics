from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_ALERT_COLUMNS = [
    "alert_id",
    "transaction_id",
    "alert_timestamp",
    "alert_outcome",
    "confirmed_fraud_flag",
]

REQUIRED_TRANSACTION_COLUMNS = [
    "transaction_id",
]

REQUIRED_COLUMNS = [
    "case_key",
    "case_id",
    "alert_id",
    "transaction_id",
    "case_created_timestamp",
    "case_priority",
    "case_status",
    "case_closed_timestamp",
    "case_outcome",
    "investigation_duration",
]

CASE_PRIORITIES = [
    "High",
    "Medium",
    "Low",
]

CASE_STATUSES = [
    "Open",
    "Closed",
]

CASE_OUTCOMES = [
    "Confirmed Fraud",
    "No Fraud",
    "Inconclusive",
]


def _validate_inputs(
    transactions: pd.DataFrame,
    alerts: pd.DataFrame,
) -> None:

    if transactions is None or transactions.empty:
        raise ValueError("transactions must not be empty")

    if alerts is None or alerts.empty:
        raise ValueError("alerts must not be empty")

    missing_transactions = [
        column
        for column in REQUIRED_TRANSACTION_COLUMNS
        if column not in transactions.columns
    ]

    if missing_transactions:
        raise ValueError(
            "transactions is missing required columns: "
            f"{missing_transactions}"
        )

    missing_alerts = [
        column
        for column in REQUIRED_ALERT_COLUMNS
        if column not in alerts.columns
    ]

    if missing_alerts:
        raise ValueError(
            "alerts is missing required columns: "
            f"{missing_alerts}"
        )

    if alerts["alert_id"].isna().any():
        raise ValueError(
            "alert_id must not contain null values"
        )

    if alerts["transaction_id"].isna().any():
        raise ValueError(
            "alert transaction_id must not contain null values"
        )

    if transactions["transaction_id"].isna().any():
        raise ValueError(
            "transaction_id must not contain null values"
        )

    if not transactions["transaction_id"].is_unique:
        raise ValueError(
            "transaction_id must be unique"
        )

    if not alerts["alert_id"].is_unique:
        raise ValueError(
            "alert_id must be unique"
        )

    transaction_ids = set(
        transactions["transaction_id"]
    )

    invalid_transaction_ids = set(
        alerts["transaction_id"]
    ) - transaction_ids

    if invalid_transaction_ids:
        raise ValueError(
            "alerts contain transaction_id values "
            "not present in transactions"
        )


def _assign_priority(
    confirmed_fraud: bool,
    alert_outcome: str,
    rng: np.random.Generator,
) -> str:

    if confirmed_fraud:
        probabilities = [0.70, 0.30, 0.00]
    elif alert_outcome == "False Positive":
        probabilities = [0.08, 0.37, 0.55]
    else:
        probabilities = [0.15, 0.40, 0.45]

    return str(
        rng.choice(
            CASE_PRIORITIES,
            p=probabilities,
        )
    )


def _assign_status(
    priority: str,
    rng: np.random.Generator,
) -> str:

    if priority == "High":
        probabilities = [0.25, 0.75]
    elif priority == "Medium":
        probabilities = [0.30, 0.70]
    else:
        probabilities = [0.40, 0.60]

    return str(
        rng.choice(
            CASE_STATUSES,
            p=probabilities,
        )
    )


def _assign_outcome(
    confirmed_fraud: bool,
    status: str,
    rng: np.random.Generator,
) -> str:

    if status == "Open":
        return "Inconclusive"

    if confirmed_fraud:
        probabilities = [0.90, 0.03, 0.07]
    else:
        probabilities = [0.02, 0.88, 0.10]

    return str(
        rng.choice(
            CASE_OUTCOMES,
            p=probabilities,
        )
    )


def generate_investigation_cases(
    transactions: pd.DataFrame,
    alerts: pd.DataFrame,
    seed: int = 20260817,
) -> pd.DataFrame:
    """
    Generate synthetic investigation cases from fraud-monitoring alerts.

    Grain:
        One row per investigation case.

    Relationship:
        Each generated investigation case is associated with one alert
        and one transaction.
    """

    _validate_inputs(
        transactions=transactions,
        alerts=alerts,
    )

    rng = np.random.default_rng(seed)

    alert_data = alerts.copy(deep=True)

    alert_data["alert_timestamp"] = pd.to_datetime(
        alert_data["alert_timestamp"]
    )

    alert_data = alert_data.sort_values(
        "alert_id"
    ).reset_index(drop=True)

    cases: list[dict] = []

    for position, alert in alert_data.iterrows():

        confirmed_fraud = bool(
            alert["confirmed_fraud_flag"]
        )

        alert_timestamp = pd.Timestamp(
            alert["alert_timestamp"]
        )

        priority = _assign_priority(
            confirmed_fraud=confirmed_fraud,
            alert_outcome=str(alert["alert_outcome"]),
            rng=rng,
        )

        status = _assign_status(
            priority=priority,
            rng=rng,
        )

        outcome = _assign_outcome(
            confirmed_fraud=confirmed_fraud,
            status=status,
            rng=rng,
        )

        # Case creation occurs after the alert.
        creation_delay_hours = int(
            rng.integers(1, 49)
        )

        case_created_timestamp = (
            alert_timestamp
            + pd.Timedelta(
                hours=creation_delay_hours
            )
        )

        if status == "Closed":

            duration_hours = int(
                rng.integers(4, 241)
            )

            case_closed_timestamp = (
                case_created_timestamp
                + pd.Timedelta(
                    hours=duration_hours
                )
            )

            investigation_duration = float(
                duration_hours / 24.0
            )

        else:

            case_closed_timestamp = pd.NaT
            investigation_duration = np.nan

        cases.append(
            {
                "case_key": position + 1,
                "case_id": f"CASE{position + 1:09d}",
                "alert_id": alert["alert_id"],
                "transaction_id": alert["transaction_id"],
                "case_created_timestamp": (
                    case_created_timestamp
                ),
                "case_priority": priority,
                "case_status": status,
                "case_closed_timestamp": (
                    case_closed_timestamp
                ),
                "case_outcome": outcome,
                "investigation_duration": (
                    investigation_duration
                ),
            }
        )

    result = pd.DataFrame(cases)

    result["case_created_timestamp"] = pd.to_datetime(
        result["case_created_timestamp"]
    )

    result["case_closed_timestamp"] = pd.to_datetime(
        result["case_closed_timestamp"]
    )

    return result[REQUIRED_COLUMNS]
