from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_TRANSACTION_COLUMNS = [
    "transaction_id",
    "transaction_amount",
]


FRAUD_SCENARIOS = [
    "account_takeover",
    "high_value",
    "high_velocity",
    "new_device",
    "geographic_anomaly",
    "online_fraud",
    "merchant_risk",
    "behavioural_deviation",
]


REQUIRED_COLUMNS = [
    "transaction_id",
    "transaction_amount",
    "fraud_flag",
    "fraud_type",
    "fraud_loss_amount",
]


def _validate_inputs(
    transactions: pd.DataFrame,
    target_prevalence: float,
) -> None:
    if transactions is None or transactions.empty:
        raise ValueError("transactions must contain at least one row")

    if not 0 <= target_prevalence <= 1:
        raise ValueError(
        "target_prevalence must be between 0 and 1"
    )

    missing_columns = [
        column
        for column in REQUIRED_TRANSACTION_COLUMNS
        if column not in transactions.columns
    ]

    if missing_columns:
        raise ValueError(
            f"transactions is missing required columns: {missing_columns}"
        )

    if transactions["transaction_id"].isna().any():
        raise ValueError(
            "transaction_id must not contain null values"
        )

    if not transactions["transaction_id"].is_unique:
        raise ValueError(
            "transaction_id must be unique"
        )

    if transactions["transaction_amount"].isna().any():
        raise ValueError(
            "transaction_amount must not contain null values"
        )

    if (transactions["transaction_amount"] <= 0).any():
        raise ValueError(
            "transaction_amount must be greater than zero"
        )


def _calculate_risk_scores(
    transactions: pd.DataFrame,
) -> np.ndarray:
    """
    Calculate synthetic risk scores using transaction-level signals.

    The score is intentionally probabilistic rather than deterministic.
    """

    amount = transactions["transaction_amount"].to_numpy(
        dtype=float,
        copy=True,
    )

    # Relative amount signal.
    amount_median = float(np.median(amount))

    if amount_median <= 0:
        amount_signal = np.zeros(len(transactions))
    else:
        amount_signal = np.clip(
            np.log1p(amount / amount_median),
            0,
            4,
        )

    # Optional transaction-channel signal.
    if "transaction_channel" in transactions.columns:
        channel_signal = (
            transactions["transaction_channel"]
            .astype(str)
            .isin(["Online", "Mobile"])
            .to_numpy(dtype=float)
        )
    else:
        channel_signal = np.zeros(len(transactions))

    # Optional transaction-type signal.
    if "transaction_type" in transactions.columns:
        type_signal = (
            transactions["transaction_type"]
            .astype(str)
            .isin(["Transfer", "Purchase"])
            .to_numpy(dtype=float)
        )
    else:
        type_signal = np.zeros(len(transactions))

    # Optional device signal.
    if "device_id" in transactions.columns:
        device_signal = (
            transactions["device_id"]
            .astype(str)
            .str.endswith(("000", "001", "002"))
            .to_numpy(dtype=float)
        )
    else:
        device_signal = np.zeros(len(transactions))

    risk_score = (
        0.45 * amount_signal
        + 0.20 * channel_signal
        + 0.15 * type_signal
        + 0.10 * device_signal
    )

    # Keep a meaningful baseline for all transactions.
    return risk_score


def _assign_fraud_scenarios(
    fraud_positions: np.ndarray,
    transactions: pd.DataFrame,
    rng: np.random.Generator,
) -> np.ndarray:
    """Assign one synthetic scenario to each confirmed fraud transaction."""

    if len(fraud_positions) == 0:
        return np.array([], dtype=object)

    scenario_weights = np.array(
        [
            0.20,  # account takeover
            0.15,  # high value
            0.15,  # high velocity
            0.15,  # new device
            0.10,  # geographic anomaly
            0.10,  # online fraud
            0.05,  # merchant risk
            0.10,  # behavioural deviation
        ],
        dtype=float,
    )

    scenario_weights /= scenario_weights.sum()

    scenarios = rng.choice(
        FRAUD_SCENARIOS,
        size=len(fraud_positions),
        p=scenario_weights,
    )

    # Ensure a non-trivial set of scenarios for sufficiently large
    # fraud populations. This prevents the synthetic dataset from
    # accidentally containing only one or two fraud types.
    if len(fraud_positions) >= 8:
        for index, scenario in enumerate(FRAUD_SCENARIOS):
            scenarios[index] = scenario

    return scenarios


def simulate_fraud(
    transactions: pd.DataFrame,
    seed: int = 20260817,
    target_prevalence: float = 0.015,
    prevalence: float | None = None,
) -> pd.DataFrame:
    """
    Apply synthetic fraud scenarios to a transaction population.

    Grain:
        One row per transaction.

    Fraud is selected probabilistically using transaction-level risk
    signals. Fraud indicators therefore overlap with legitimate activity.
    """
    if prevalence is not None:
        target_prevalence = prevalence

    _validate_inputs(
        transactions,
        target_prevalence,
    )

    rng = np.random.default_rng(seed)

    result = transactions.copy(deep=True)

    count = len(result)

    target_fraud_count = int(
        round(count * target_prevalence)
    )

    risk_scores = _calculate_risk_scores(result)

    # Add stochastic variation so that identical risk signals do not
    # deterministically imply fraud.
    stochastic_score = rng.random(count)

    ranking_score = (
        risk_scores
        + stochastic_score * 0.75
    )

    fraud_flag = np.zeros(
        count,
        dtype=bool,
    )

    if target_fraud_count > 0:
        selected_positions = np.argsort(
            ranking_score
        )[-target_fraud_count:]

        fraud_flag[selected_positions] = True
    else:
        selected_positions = np.array(
            [],
            dtype=int,
        )

    fraud_scenario = np.full(
        count,
        None,
        dtype=object,
    )

    FRAUD_TYPE_MAP = {
    "high_value": "High Value",
    "high_velocity": "High Velocity",
    "new_device": "New Device",
    "geographic_anomaly": "Geographic Anomaly",
    "online_fraud": "Online Fraud",
    "merchant_risk": "Merchant Risk",
    "behavioural_deviation": "Behavioural Deviation",
    }

    assigned_scenarios = _assign_fraud_scenarios(
        selected_positions,
        result,
        rng,
    )

    if len(selected_positions) > 0:
        fraud_scenario[selected_positions] = assigned_scenarios

    fraud_loss_amount = np.zeros(
    count,
    dtype=float,
    )

    if len(selected_positions) > 0:
        transaction_amounts = result.loc[
        result.index[selected_positions],
        "transaction_amount",
    ].to_numpy(dtype=float)

    loss_fraction = rng.uniform(
        0.35,
        1.00,
        size=len(selected_positions),
    )

    fraud_losses = np.round(
        transaction_amounts * loss_fraction,
        2,
    )

    fraud_loss_amount[selected_positions] = fraud_losses

    result["fraud_flag"] = fraud_flag
    result["fraud_type"] = fraud_scenario
    result["fraud_loss_amount"] = fraud_loss_amount

    return result[REQUIRED_COLUMNS]
