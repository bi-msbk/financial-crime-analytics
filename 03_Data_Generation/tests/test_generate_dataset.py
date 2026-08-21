from __future__ import annotations

import pandas as pd
import pytest

from pipeline.generate_dataset import (
    REQUIRED_DATASETS,
    generate_dataset,
)


def test_generate_dataset_returns_dictionary():
    result = generate_dataset(
        customer_count=100,
        account_count=120,
        merchant_count=25,
        device_count=150,
        geography_count=20,
        transaction_count=250,
        seed=20260817,
    )

    assert isinstance(result, dict)


def test_generate_dataset_has_required_datasets():
    result = generate_dataset(
        customer_count=100,
        account_count=120,
        merchant_count=25,
        device_count=150,
        geography_count=20,
        transaction_count=250,
        seed=20260817,
    )

    assert set(REQUIRED_DATASETS).issubset(result.keys())


def test_all_generated_objects_are_dataframes():
    result = generate_dataset(
        customer_count=100,
        account_count=120,
        merchant_count=25,
        device_count=150,
        geography_count=20,
        transaction_count=250,
        seed=20260817,
    )

    for name in REQUIRED_DATASETS:
        assert isinstance(result[name], pd.DataFrame)


def test_dataset_row_counts_are_correct():
    result = generate_dataset(
        customer_count=100,
        account_count=120,
        merchant_count=25,
        device_count=150,
        geography_count=20,
        transaction_count=250,
        seed=20260817,
    )

    assert len(result["customer"]) == 100
    assert len(result["account"]) == 120
    assert len(result["merchant"]) == 25
    assert len(result["device"]) == 150
    assert len(result["geography"]) == 20
    assert len(result["transaction"]) == 250


def test_transaction_population_is_fraud_simulated():
    result = generate_dataset(
        customer_count=100,
        account_count=120,
        merchant_count=25,
        device_count=150,
        geography_count=20,
        transaction_count=250,
        seed=20260817,
    )

    transactions = result["transaction"]

    assert "fraud_flag" in transactions.columns
    assert "fraud_scenario" in transactions.columns
    assert "fraud_loss_amount" in transactions.columns


def test_fraud_outcomes_exist_for_fraud_transactions():
    result = generate_dataset(
        customer_count=100,
        account_count=120,
        merchant_count=25,
        device_count=150,
        geography_count=20,
        transaction_count=250,
        seed=20260817,
    )

    transactions = result["transaction"]
    outcomes = result["fraud_outcome"]

    fraud_ids = set(
        transactions.loc[
            transactions["fraud_flag"].astype(bool),
            "transaction_id",
        ]
    )

    outcome_ids = set(outcomes["transaction_id"])

    assert fraud_ids == outcome_ids


def test_control_evaluation_is_present():
    result = generate_dataset(
        customer_count=100,
        account_count=120,
        merchant_count=25,
        device_count=150,
        geography_count=20,
        transaction_count=250,
        seed=20260817,
    )

    assert not result["control_evaluation"].empty


def test_investigation_cases_are_present():
    result = generate_dataset(
        customer_count=100,
        account_count=120,
        merchant_count=25,
        device_count=150,
        geography_count=20,
        transaction_count=250,
        seed=20260817,
    )

    assert not result["investigation"].empty


def test_generate_dataset_is_reproducible():
    result_1 = generate_dataset(
        customer_count=100,
        account_count=120,
        merchant_count=25,
        device_count=150,
        geography_count=20,
        transaction_count=250,
        seed=20260817,
    )

    result_2 = generate_dataset(
        customer_count=100,
        account_count=120,
        merchant_count=25,
        device_count=150,
        geography_count=20,
        transaction_count=250,
        seed=20260817,
    )

    for name in REQUIRED_DATASETS:
        pd.testing.assert_frame_equal(
            result_1[name],
            result_2[name],
        )


def test_different_seed_changes_generated_transactions():
    result_1 = generate_dataset(
        customer_count=100,
        account_count=120,
        merchant_count=25,
        device_count=150,
        geography_count=20,
        transaction_count=250,
        seed=20260817,
    )

    result_2 = generate_dataset(
        customer_count=100,
        account_count=120,
        merchant_count=25,
        device_count=150,
        geography_count=20,
        transaction_count=250,
        seed=20260818,
    )

    assert not result_1["transaction"].equals(
        result_2["transaction"]
    )


def test_invalid_transaction_count_is_rejected():
    with pytest.raises(ValueError):
        generate_dataset(
            customer_count=100,
            account_count=120,
            merchant_count=25,
            device_count=150,
            geography_count=20,
            transaction_count=0,
            seed=20260817,
        )
