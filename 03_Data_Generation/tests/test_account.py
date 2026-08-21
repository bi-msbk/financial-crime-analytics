import pandas as pd
import pytest

from src.generators.account import generate_accounts
from src.generators.customer import generate_customers


SEED = 20260817
CUSTOMER_COUNT = 500
ACCOUNT_COUNT = 650
START_DATE = "2024-01-01"
END_DATE = "2025-12-31"


@pytest.fixture
def customers():
    return generate_customers(
        count=CUSTOMER_COUNT,
        seed=SEED,
        start_date=START_DATE,
        end_date=END_DATE,
    )


@pytest.fixture
def accounts(customers):
    return generate_accounts(
        customers=customers,
        count=ACCOUNT_COUNT,
        seed=SEED,
        start_date=START_DATE,
        end_date=END_DATE,
    )


def test_account_returns_dataframe(accounts):
    assert isinstance(accounts, pd.DataFrame)


def test_account_has_required_columns(accounts):
    required = {
        "account_key",
        "account_id",
        "customer_key",
        "customer_id",
        "account_type",
        "account_status",
        "account_open_date",
        "account_region",
    }

    assert required.issubset(accounts.columns)


def test_account_has_expected_row_count(accounts):
    assert len(accounts) == ACCOUNT_COUNT


def test_account_keys_are_unique(accounts):
    assert accounts["account_key"].is_unique


def test_account_identifiers_are_unique(accounts):
    assert accounts["account_id"].is_unique


def test_account_identifiers_are_not_null(accounts):
    assert accounts["account_key"].notna().all()
    assert accounts["account_id"].notna().all()
    assert accounts["customer_key"].notna().all()
    assert accounts["customer_id"].notna().all()


def test_account_identifier_format(accounts):
    assert accounts["account_id"].str.match(r"^ACC\d{6}$").all()


def test_account_customer_keys_exist(accounts, customers):
    assert accounts["customer_key"].isin(
        customers["customer_key"]
    ).all()


def test_account_customer_ids_exist(accounts, customers):
    assert accounts["customer_id"].isin(
        customers["customer_id"]
    ).all()


def test_account_customer_relationship_is_consistent(accounts, customers):
    customer_lookup = customers.set_index("customer_key")["customer_id"]

    expected_customer_ids = accounts["customer_key"].map(customer_lookup)

    assert (
        accounts["customer_id"].reset_index(drop=True)
        == expected_customer_ids.reset_index(drop=True)
    ).all()


def test_account_types_are_valid(accounts):
    allowed = {
        "Current",
        "Savings",
        "Credit",
    }

    assert accounts["account_type"].isin(allowed).all()


def test_account_statuses_are_valid(accounts):
    allowed = {
        "Active",
        "Closed",
        "Dormant",
    }

    assert accounts["account_status"].isin(allowed).all()


def test_account_open_dates_are_valid(accounts):
    dates = pd.to_datetime(accounts["account_open_date"])

    assert dates.min() >= pd.Timestamp(START_DATE)
    assert dates.max() <= pd.Timestamp(END_DATE)


def test_account_open_date_is_not_before_customer_onboarding(
    accounts,
    customers,
):
    customer_lookup = customers.set_index("customer_key")[
        "customer_onboarding_date"
    ]

    onboarding_dates = pd.to_datetime(
        accounts["customer_key"].map(customer_lookup)
    )

    account_dates = pd.to_datetime(accounts["account_open_date"])

    assert (account_dates >= onboarding_dates).all()


def test_account_generation_is_reproducible(customers):
    first = generate_accounts(
        customers=customers,
        count=ACCOUNT_COUNT,
        seed=SEED,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    second = generate_accounts(
        customers=customers,
        count=ACCOUNT_COUNT,
        seed=SEED,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    pd.testing.assert_frame_equal(first, second)


def test_different_seed_changes_generated_attributes(customers):
    first = generate_accounts(
        customers=customers,
        count=ACCOUNT_COUNT,
        seed=SEED,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    second = generate_accounts(
        customers=customers,
        count=ACCOUNT_COUNT,
        seed=SEED + 1,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    assert not first.equals(second)


def test_invalid_count_is_rejected(customers):
    with pytest.raises(ValueError):
        generate_accounts(
            customers=customers,
            count=0,
            seed=SEED,
            start_date=START_DATE,
            end_date=END_DATE,
        )


def test_empty_customers_are_rejected():
    empty_customers = pd.DataFrame()

    with pytest.raises(ValueError):
        generate_accounts(
            customers=empty_customers,
            count=10,
            seed=SEED,
            start_date=START_DATE,
            end_date=END_DATE,
        )
