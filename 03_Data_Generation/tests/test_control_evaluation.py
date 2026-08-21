from __future__ import annotations

import pandas as pd
import pytest

from generators.customer import generate_customer
from generators.account import generate_accounts
from generators.merchant import generate_merchants
from generators.device import generate_devices
from generators.geography import generate_geography
from generators.date import generate_date
from generators.transaction import generate_transactions

from fraud.fraud_simulation import simulate_fraud
from fraud.fraud_outcome import generate_fraud_outcomes

from controls.control_evaluation import (
    REQUIRED_COLUMNS,
    evaluate_controls,
)


START_DATE = "2024-01-01"
END_DATE = "2025-12-31"
SEED = 20260817


def build_control_input():
    customers = generate_customer(
        count=500,
        seed=SEED,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    accounts = generate_accounts(
        customers=customers,
        count=650,
        seed=SEED,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    merchants = generate_merchants(
        count=100,
        seed=SEED,
    )

    devices = generate_devices(
        count=750,
        seed=SEED,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    geography = generate_geography(
        count=50,
        seed=SEED,
    )

    dates = generate_date(
        START_DATE,
        END_DATE,
    )

    transactions = generate_transactions(
        customers=customers,
        accounts=accounts,
        merchants=merchants,
        devices=devices,
        geography=geography,
        dates=dates,
        count=1000,
        seed=SEED,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    return simulate_fraud(
        transactions=transactions,
        target_prevalence=0.015,
        seed=SEED,
    )


def test_control_evaluation_returns_dataframe():
    transactions = build_control_input()

    result = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    assert isinstance(result, pd.DataFrame)


def test_control_evaluation_has_required_columns():
    transactions = build_control_input()

    result = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    assert list(result.columns) == REQUIRED_COLUMNS


def test_control_evaluation_contains_valid_transaction_ids():
    transactions = build_control_input()

    result = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    assert result["transaction_id"].isin(
        transactions["transaction_id"]
    ).all()


def test_control_evaluation_contains_valid_rule_ids():
    transactions = build_control_input()

    result = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    assert result["rule_id"].notna().all()
    assert result["rule_id"].astype(str).str.startswith("RULE").all()


def test_control_evaluation_allows_multiple_alerts_per_transaction():
    transactions = build_control_input()

    result = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    alert_counts = result.groupby(
        "transaction_id"
    ).size()

    assert (alert_counts >= 1).all()


def test_control_evaluation_has_valid_alert_statuses():
    transactions = build_control_input()

    result = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    valid_statuses = {
        "Generated",
    }

    assert set(result["alert_status"]).issubset(
        valid_statuses
    )


def test_control_evaluation_has_valid_alert_outcomes():
    transactions = build_control_input()

    result = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    valid_outcomes = {
        "True Positive",
        "False Positive",
    }

    assert set(result["alert_outcome"]).issubset(
        valid_outcomes
    )


def test_confirmed_fraud_flag_matches_transaction():
    transactions = build_control_input()

    result = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    fraud_lookup = transactions.set_index(
        "transaction_id"
    )["fraud_flag"]

    expected = result["transaction_id"].map(
        fraud_lookup
    )

    assert (
        result["confirmed_fraud_flag"].astype(bool)
        == expected.astype(bool)
    ).all()


def test_true_positive_alerts_are_fraudulent():
    transactions = build_control_input()

    result = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    true_positive = result[
        result["alert_outcome"] == "True Positive"
    ]

    if not true_positive.empty:
        assert true_positive[
            "confirmed_fraud_flag"
        ].astype(bool).all()


def test_false_positive_alerts_are_non_fraud():
    transactions = build_control_input()

    result = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    false_positive = result[
        result["alert_outcome"] == "False Positive"
    ]

    if not false_positive.empty:
        assert (
            ~false_positive[
                "confirmed_fraud_flag"
            ].astype(bool)
        ).all()


def test_alert_ids_are_unique():
    transactions = build_control_input()

    result = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    assert result["alert_id"].is_unique


def test_alert_timestamps_are_valid():
    transactions = build_control_input()

    result = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    timestamps = pd.to_datetime(
        result["alert_timestamp"]
    )

    assert timestamps.notna().all()


def test_control_evaluation_is_reproducible():
    transactions = build_control_input()

    result_one = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    result_two = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    pd.testing.assert_frame_equal(
        result_one,
        result_two,
    )


def test_different_seed_changes_control_results():
    transactions = build_control_input()

    result_one = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    result_two = evaluate_controls(
        transactions=transactions,
        seed=SEED + 1,
    )

    assert not result_one.equals(result_two)


def test_empty_transactions_are_rejected():
    with pytest.raises(ValueError):
        evaluate_controls(
            transactions=pd.DataFrame(),
            seed=SEED,
        )


def test_missing_required_column_is_rejected():
    transactions = build_control_input().drop(
        columns=["transaction_id"]
    )

    with pytest.raises(ValueError):
        evaluate_controls(
            transactions=transactions,
            seed=SEED,
        )
