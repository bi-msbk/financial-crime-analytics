from __future__ import annotations

import pandas as pd
import pytest

from pipeline.generate_dataset import generate_dataset


SEED = 20260817


@pytest.fixture(scope="module")
def dataset():
    return generate_dataset(
        customer_count=100,
        account_count=120,
        merchant_count=25,
        device_count=150,
        geography_count=20,
        transaction_count=250,
        seed=SEED,
    )


def test_all_expected_datasets_exist(dataset):
    expected = {
        "customer",
        "account",
        "merchant",
        "device",
        "geography",
        "date",
        "transaction",
        "customer_behaviour",
        "fraud_outcome",
        "control_evaluation",
        "investigation",
    }

    assert expected.issubset(dataset.keys())


def test_all_datasets_are_dataframes(dataset):
    for name, df in dataset.items():
        assert isinstance(df, pd.DataFrame), name


def test_customer_account_relationships(dataset):
    customers = dataset["customer"]
    accounts = dataset["account"]

    assert accounts["customer_key"].isin(
        customers["customer_key"]
    ).all()

    assert accounts["customer_id"].isin(
        customers["customer_id"]
    ).all()


def test_transaction_customer_relationship(dataset):
    customers = dataset["customer"]
    transactions = dataset["transaction"]

    assert transactions["customer_key"].isin(
        customers["customer_key"]
    ).all()


def test_transaction_account_relationship(dataset):
    accounts = dataset["account"]
    transactions = dataset["transaction"]

    assert transactions["account_key"].isin(
        accounts["account_key"]
    ).all()


def test_transaction_merchant_relationship(dataset):
    merchants = dataset["merchant"]
    transactions = dataset["transaction"]

    assert transactions["merchant_key"].isin(
        merchants["merchant_key"]
    ).all()


def test_transaction_device_relationship(dataset):
    devices = dataset["device"]
    transactions = dataset["transaction"]

    assert transactions["device_key"].isin(
        devices["device_key"]
    ).all()


def test_transaction_geography_relationship(dataset):
    geography = dataset["geography"]
    transactions = dataset["transaction"]

    assert transactions["geography_key"].isin(
        geography["geography_key"]
    ).all()


def test_transaction_dates_are_valid(dataset):
    dates = dataset["date"]
    transactions = dataset["transaction"]

    assert transactions["date_key"].isin(
        dates["date_key"]
    ).all()


def test_fraud_transactions_have_fraud_attributes(dataset):
    transactions = dataset["transaction"]

    fraud = transactions[
        transactions["fraud_flag"].astype(bool)
    ]

    assert not fraud.empty

    assert fraud["fraud_scenario"].notna().all()
    assert fraud["fraud_loss_amount"].ge(0).all()


def test_non_fraud_transactions_have_zero_loss(dataset):
    transactions = dataset["transaction"]

    non_fraud = transactions[
        ~transactions["fraud_flag"].astype(bool)
    ]

    assert (
        non_fraud["fraud_loss_amount"] == 0
    ).all()


def test_fraud_outcomes_reference_transactions(dataset):
    transactions = dataset["transaction"]
    outcomes = dataset["fraud_outcome"]

    assert outcomes["transaction_id"].isin(
        transactions["transaction_id"]
    ).all()


def test_fraud_outcomes_only_reference_fraud(dataset):
    transactions = dataset["transaction"]
    outcomes = dataset["fraud_outcome"]

    fraud_transaction_ids = set(
        transactions.loc[
            transactions["fraud_flag"].astype(bool),
            "transaction_id",
        ]
    )

    assert set(
        outcomes["transaction_id"]
    ).issubset(fraud_transaction_ids)


def test_control_alerts_reference_transactions(dataset):
    transactions = dataset["transaction"]
    controls = dataset["control_evaluation"]

    assert controls["transaction_id"].isin(
        transactions["transaction_id"]
    ).all()


def test_investigations_reference_alerts(dataset):
    alerts = dataset["control_evaluation"]
    investigations = dataset["investigation"]

    assert investigations["alert_id"].isin(
        alerts["alert_id"]
    ).all()


def test_investigation_transactions_are_valid(dataset):
    transactions = dataset["transaction"]
    investigations = dataset["investigation"]

    assert investigations["transaction_id"].isin(
        transactions["transaction_id"]
    ).all()


def test_fraud_outcome_loss_matches_transaction(dataset):
    transactions = dataset["transaction"]
    outcomes = dataset["fraud_outcome"]

    transaction_loss = transactions.set_index(
        "transaction_id"
    )["fraud_loss_amount"]

    for _, outcome in outcomes.iterrows():
        transaction_id = outcome["transaction_id"]

        assert outcome["fraud_loss_amount"] == pytest.approx(
            transaction_loss.loc[transaction_id]
        )


def test_transaction_ids_are_unique(dataset):
    transactions = dataset["transaction"]

    assert transactions["transaction_id"].is_unique


def test_fraud_outcome_transaction_ids_are_unique(dataset):
    outcomes = dataset["fraud_outcome"]

    assert outcomes["transaction_id"].is_unique


def test_control_alert_ids_are_unique(dataset):
    controls = dataset["control_evaluation"]

    assert controls["alert_id"].is_unique


def test_investigation_case_ids_are_unique(dataset):
    investigations = dataset["investigation"]

    assert investigations["case_id"].is_unique
