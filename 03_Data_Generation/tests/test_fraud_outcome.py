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

from fraud.fraud_outcome import (
    FRAUD_OUTCOME_SOURCES,
    FRAUD_TYPES,
    REQUIRED_COLUMNS,
    generate_fraud_outcomes,
)


START_DATE = "2024-01-01"
END_DATE = "2025-12-31"
SEED = 20260817


def build_fraud_transactions():
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
        prevalence=0.015,
        seed=SEED,
    )
def test_fraud_outcome_returns_dataframe():
    transactions = build_fraud_transactions()

    result = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    assert isinstance(result, pd.DataFrame)


def test_fraud_outcome_has_required_columns():
    transactions = build_fraud_transactions()

    result = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    assert list(result.columns) == REQUIRED_COLUMNS


def test_one_outcome_per_fraud_transaction():
    transactions = build_fraud_transactions()

    result = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    fraud_count = int(
        transactions["fraud_flag"].sum()
    )

    assert len(result) == fraud_count


def test_outcome_keys_are_unique():
    transactions = build_fraud_transactions()

    result = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    assert result["fraud_outcome_key"].is_unique


def test_outcome_ids_are_unique():
    transactions = build_fraud_transactions()

    result = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    assert result["fraud_outcome_id"].is_unique


def test_transaction_ids_are_unique():
    transactions = build_fraud_transactions()

    result = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    assert result["transaction_id"].is_unique


def test_outcome_transaction_ids_exist():
    transactions = build_fraud_transactions()

    result = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    valid_ids = set(
        transactions["transaction_id"]
    )

    assert set(
        result["transaction_id"]
    ).issubset(valid_ids)


def test_only_fraud_transactions_receive_outcomes():
    transactions = build_fraud_transactions()

    result = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    expected_ids = set(
        transactions.loc[
            transactions["fraud_flag"],
            "transaction_id",
        ]
    )

    actual_ids = set(
        result["transaction_id"]
    )

    assert actual_ids == expected_ids


def test_fraud_types_are_valid():
    transactions = build_fraud_transactions()

    result = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    assert set(
        result["fraud_type"]
    ).issubset(FRAUD_TYPES)


def test_fraud_sources_are_valid():
    transactions = build_fraud_transactions()

    result = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    assert set(
        result["fraud_outcome_source"]
    ).issubset(FRAUD_OUTCOME_SOURCES)


def test_fraud_loss_is_non_negative():
    transactions = build_fraud_transactions()

    result = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    assert (
        result["fraud_loss_amount"] >= 0
    ).all()


def test_fraud_loss_matches_transaction():
    transactions = build_fraud_transactions()

    result = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    expected = transactions.loc[
        transactions["fraud_flag"],
        [
            "transaction_id",
            "fraud_loss_amount",
        ],
    ]

    merged = result.merge(
        expected,
        on="transaction_id",
        suffixes=(
            "_outcome",
            "_transaction",
        ),
    )

    assert (
        merged["fraud_loss_amount_outcome"]
        == merged["fraud_loss_amount_transaction"]
    ).all()


def test_confirmed_dates_are_valid():
    transactions = build_fraud_transactions()

    result = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    assert pd.api.types.is_datetime64_any_dtype(
        result["fraud_confirmed_date"]
    )


def test_outcome_keys_are_sequential():
    transactions = build_fraud_transactions()

    result = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    expected = list(
        range(
            1,
            len(result) + 1,
        )
    )

    assert (
        result["fraud_outcome_key"].tolist()
        == expected
    )


def test_generation_is_reproducible():
    transactions = build_fraud_transactions()

    first = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    second = generate_fraud_outcomes(
        transactions=transactions,
        seed=SEED,
    )

    pd.testing.assert_frame_equal(
        first,
        second,
    )


def test_empty_transactions_are_rejected():
    empty = pd.DataFrame()

    with pytest.raises(ValueError):
        generate_fraud_outcomes(empty)


def test_missing_required_column_is_rejected():
    transactions = build_fraud_transactions()

    broken = transactions.drop(
        columns=["fraud_flag"]
    )

    with pytest.raises(ValueError):
        generate_fraud_outcomes(broken)
