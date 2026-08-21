from __future__ import annotations

import pandas as pd
import pytest

from src.fraud.fraud_simulation import (
    FRAUD_SCENARIOS,
    REQUIRED_COLUMNS,
    simulate_fraud,
)

from src.generators.customer import generate_customer
from src.generators.account import generate_accounts
from src.generators.merchant import generate_merchants
from src.generators.device import generate_devices
from src.generators.geography import generate_geography
from src.generators.date import generate_date
from src.generators.transaction import generate_transactions
from src.behaviour.customer_behaviour import (
    generate_customer_behaviour_profiles,
)


SEED = 20260817
CUSTOMER_COUNT = 500
ACCOUNT_COUNT = 650
MERCHANT_COUNT = 100
DEVICE_COUNT = 750
TRANSACTION_COUNT = 5000

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"


@pytest.fixture
def transaction_data():
    customers = generate_customer(
        count=CUSTOMER_COUNT,
        seed=SEED,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    accounts = generate_accounts(
        customers=customers,
        count=ACCOUNT_COUNT,
        seed=SEED,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    merchants = generate_merchants(
        count=MERCHANT_COUNT,
        seed=SEED,
    )

    devices = generate_devices(
        count=DEVICE_COUNT,
        seed=SEED,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    geography = generate_geography(
        count=20,
        seed=SEED,
    )

    dates = generate_date(
        START_DATE,
        END_DATE,
    )

    behaviour = generate_customer_behaviour_profiles(
        customers,
        seed=SEED,
    )

    return generate_transactions(
        count=TRANSACTION_COUNT,
        customers=customers,
        accounts=accounts,
        merchants=merchants,
        devices=devices,
        geography=geography,
        dates=dates,
        seed=SEED,
        start_date=START_DATE,
        end_date=END_DATE,
        behaviour=behaviour,
    )


def test_fraud_returns_dataframe(transaction_data):
    result = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=0.015,
    )

    assert isinstance(result, pd.DataFrame)


def test_fraud_has_required_columns(transaction_data):
    result = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=0.015,
    )

    assert list(result.columns) == REQUIRED_COLUMNS


def test_fraud_preserves_transaction_count(transaction_data):
    result = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=0.015,
    )

    assert len(result) == len(transaction_data)


def test_transaction_ids_are_unique(transaction_data):
    result = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=0.015,
    )

    assert result["transaction_id"].is_unique


def test_fraud_flag_is_boolean(transaction_data):
    result = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=0.015,
    )

    assert result["fraud_flag"].dtype == bool


def test_fraud_flag_contains_both_classes(transaction_data):
    result = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=0.015,
    )

    assert result["fraud_flag"].nunique() == 2


def test_fraud_prevalence_is_close_to_target(transaction_data):
    target = 0.015

    result = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=target,
    )

    prevalence = result["fraud_flag"].mean()

    # Synthetic generation tolerance.
    assert abs(prevalence - target) <= 0.01


def test_fraud_scenarios_are_valid(transaction_data):
    result = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=0.015,
    )

    fraud_rows = result.loc[result["fraud_flag"]]

    assert set(fraud_rows["fraud_type"]).issubset(
        set(FRAUD_SCENARIOS)
    )


def test_non_fraud_has_zero_loss(transaction_data):
    result = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=0.015,
    )

    non_fraud = result.loc[~result["fraud_flag"]]

    assert (non_fraud["fraud_loss_amount"] == 0).all()


def test_fraud_loss_is_non_negative(transaction_data):
    result = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=0.015,
    )

    assert (result["fraud_loss_amount"] >= 0).all()


def test_fraud_loss_does_not_exceed_transaction_amount(
    transaction_data,
):
    result = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=0.015,
    )

    fraud_rows = result.loc[result["fraud_flag"]]

    assert (
        fraud_rows["fraud_loss_amount"]
        <= fraud_rows["transaction_amount"]
    ).all()


def test_fraud_has_confirmed_outcome(transaction_data):
    result = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=0.015,
    )

    fraud_rows = result.loc[result["fraud_flag"]]

    assert fraud_rows["fraud_type"].notna().all()


def test_fraud_scenarios_are_non_trivial(transaction_data):
    result = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=0.015,
    )

    fraud_rows = result.loc[result["fraud_flag"]]

    assert fraud_rows["fraud_type"].nunique() >= 3


def test_fraud_generation_is_reproducible(transaction_data):
    result1 = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=0.015,
    )

    result2 = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=0.015,
    )

    pd.testing.assert_frame_equal(result1, result2)


def test_different_seed_changes_fraud_assignment(transaction_data):
    result1 = simulate_fraud(
        transaction_data,
        seed=SEED,
        target_prevalence=0.015,
    )

    result2 = simulate_fraud(
        transaction_data,
        seed=SEED + 1,
        target_prevalence=0.015,
    )

    assert not result1.equals(result2)


def test_invalid_prevalence_is_rejected(transaction_data):
    with pytest.raises(ValueError):
        simulate_fraud(
            transaction_data,
            seed=SEED,
            target_prevalence=1.5,
        )


def test_negative_prevalence_is_rejected(transaction_data):
    with pytest.raises(ValueError):
        simulate_fraud(
            transaction_data,
            seed=SEED,
            target_prevalence=-0.01,
        )


def test_empty_transactions_are_rejected():
    with pytest.raises(ValueError):
        simulate_fraud(
            pd.DataFrame(),
            seed=SEED,
            target_prevalence=0.015,
        )
