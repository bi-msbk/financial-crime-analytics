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
from controls.control_evaluation import evaluate_controls

from pipeline.investigation_simulation import (
    REQUIRED_COLUMNS,
    CASE_PRIORITIES,
    CASE_STATUSES,
    CASE_OUTCOMES,
    generate_investigation_cases,
)


START_DATE = "2024-01-01"
END_DATE = "2025-12-31"
SEED = 20260817


def build_investigation_input():
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

    transactions = simulate_fraud(
        transactions=transactions,
        target_prevalence=0.015,
        seed=SEED,
    )

    alerts = evaluate_controls(
        transactions=transactions,
        seed=SEED,
    )

    return transactions, alerts


def test_investigation_returns_dataframe():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    assert isinstance(result, pd.DataFrame)


def test_investigation_has_required_columns():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    assert list(result.columns) == REQUIRED_COLUMNS


def test_case_ids_are_unique():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    assert result["case_id"].is_unique


def test_case_keys_are_unique():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    assert result["case_key"].is_unique


def test_case_ids_are_not_null():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    assert result["case_id"].notna().all()


def test_alert_ids_exist():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    assert result["alert_id"].isin(
        alerts["alert_id"]
    ).all()


def test_transaction_ids_exist():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    assert result["transaction_id"].isin(
        transactions["transaction_id"]
    ).all()


def test_case_priorities_are_valid():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    assert set(result["case_priority"]).issubset(
        set(CASE_PRIORITIES)
    )


def test_case_statuses_are_valid():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    assert set(result["case_status"]).issubset(
        set(CASE_STATUSES)
    )


def test_case_outcomes_are_valid():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    assert set(result["case_outcome"]).issubset(
        set(CASE_OUTCOMES)
    )


def test_case_creation_timestamp_is_valid():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    creation = pd.to_datetime(
        result["case_created_timestamp"]
    )

    alert_lookup = alerts.set_index(
        "alert_id"
    )["alert_timestamp"]

    alert_times = pd.to_datetime(
        result["alert_id"].map(alert_lookup)
    )

    assert (creation >= alert_times).all()


def test_closed_cases_have_closed_timestamp():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    closed = result[
        result["case_status"] == "Closed"
    ]

    if not closed.empty:
        assert closed[
            "case_closed_timestamp"
        ].notna().all()


def test_open_cases_have_no_closed_timestamp():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    open_cases = result[
        result["case_status"] == "Open"
    ]

    if not open_cases.empty:
        assert open_cases[
            "case_closed_timestamp"
        ].isna().all()


def test_investigation_duration_is_non_negative():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    assert (
        result["investigation_duration"].dropna()
        >= 0
    ).all()


def test_closed_case_duration_is_present():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    closed = result[
        result["case_status"] == "Closed"
    ]

    if not closed.empty:
        assert closed[
            "investigation_duration"
        ].notna().all()


def test_high_priority_cases_exist_when_alert_population_is_sufficient():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    assert (
        result["case_priority"] == "High"
    ).any()


def test_fraud_alerts_receive_higher_case_priority():
    transactions, alerts = build_investigation_input()

    result = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    fraud_alert_ids = set(
        alerts.loc[
            alerts["confirmed_fraud_flag"].astype(bool),
            "alert_id",
        ]
    )

    fraud_cases = result[
        result["alert_id"].isin(fraud_alert_ids)
    ]

    if not fraud_cases.empty:
        assert (
            fraud_cases["case_priority"]
            .isin(["High", "Medium"])
            .all()
        )


def test_investigation_is_reproducible():
    transactions, alerts = build_investigation_input()

    result_one = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    result_two = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    pd.testing.assert_frame_equal(
        result_one,
        result_two,
    )


def test_different_seed_changes_investigation_results():
    transactions, alerts = build_investigation_input()

    result_one = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED,
    )

    result_two = generate_investigation_cases(
        transactions=transactions,
        alerts=alerts,
        seed=SEED + 1,
    )

    assert not result_one.equals(result_two)


def test_empty_alerts_are_rejected():
    transactions, alerts = build_investigation_input()

    with pytest.raises(ValueError):
        generate_investigation_cases(
            transactions=transactions,
            alerts=pd.DataFrame(),
            seed=SEED,
        )


def test_missing_alert_id_is_rejected():
    transactions, alerts = build_investigation_input()

    invalid_alerts = alerts.drop(
        columns=["alert_id"]
    )

    with pytest.raises(ValueError):
        generate_investigation_cases(
            transactions=transactions,
            alerts=invalid_alerts,
            seed=SEED,
        )
