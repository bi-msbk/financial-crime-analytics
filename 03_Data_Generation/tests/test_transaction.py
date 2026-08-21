
from __future__ import annotations

import pandas as pd
import pytest

from src.generators.account import generate_accounts
from src.generators.customer import generate_customer
from src.generators.date import generate_date
from src.generators.device import generate_devices
from src.generators.geography import generate_geography
from src.generators.merchant import generate_merchants
from src.generators.transaction import (
    REQUIRED_COLUMNS,
    TRANSACTION_CHANNELS,
    TRANSACTION_STATUSES,
    TRANSACTION_TYPES,
    generate_transactions,
)


START_DATE = "2024-01-01"
END_DATE = "2025-12-31"


@pytest.fixture
def source_data():
    customers = generate_customer(
        count=100,
        seed=20260817,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    accounts = generate_accounts(
        customers=customers,
        count=150,
        seed=20260817,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    merchants = generate_merchants(
        count=50,
        seed=20260817,
    )

    devices = generate_devices(
        count=100,
        seed=20260817,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    geography = generate_geography(
        count=12,
        seed=20260817,
    )

    dates = generate_date(
        START_DATE,
        END_DATE,
    )

    return (
        customers,
        accounts,
        merchants,
        devices,
        geography,
        dates,
    )


def make_transactions(source_data, count=500, seed=20260817):
    return generate_transactions(
        customers=source_data[0],
        accounts=source_data[1],
        merchants=source_data[2],
        devices=source_data[3],
        geography=source_data[4],
        dates=source_data[5],
        count=count,
        seed=seed,
        start_date=START_DATE,
        end_date=END_DATE,
    )


def test_transaction_returns_dataframe(source_data):
    df = make_transactions(source_data)

    assert isinstance(df, pd.DataFrame)


def test_transaction_has_required_columns(source_data):
    df = make_transactions(source_data)

    assert list(df.columns) == REQUIRED_COLUMNS


def test_transaction_has_expected_row_count(source_data):
    df = make_transactions(source_data, count=500)

    assert len(df) == 500


def test_transaction_keys_are_unique(source_data):
    df = make_transactions(source_data)

    assert df["transaction_key"].is_unique


def test_transaction_ids_are_unique(source_data):
    df = make_transactions(source_data)

    assert df["transaction_id"].is_unique


def test_transaction_identifiers_are_not_null(source_data):
    df = make_transactions(source_data)

    assert df["transaction_key"].notna().all()
    assert df["transaction_id"].notna().all()


def test_transaction_identifier_format(source_data):
    df = make_transactions(source_data)

    assert df["transaction_id"].str.match(
        r"^TXN\d{8}$"
    ).all()


def test_customer_account_relationship_is_valid(source_data):
    df = make_transactions(source_data)

    accounts = source_data[1]

    merged = df.merge(
        accounts[
            [
                "account_key",
                "customer_key",
            ]
        ],
        on="account_key",
        how="left",
        suffixes=("", "_account"),
    )

    assert merged["customer_key_account"].notna().all()

    assert (
        merged["customer_key"]
        == merged["customer_key_account"]
    ).all()


def test_customer_ids_are_valid(source_data):
    df = make_transactions(source_data)

    customers = source_data[0]

    assert set(df["customer_key"]).issubset(
        set(customers["customer_key"])
    )


def test_account_ids_are_valid(source_data):
    df = make_transactions(source_data)

    accounts = source_data[1]

    assert set(df["account_key"]).issubset(
        set(accounts["account_key"])
    )


def test_merchant_ids_are_valid(source_data):
    df = make_transactions(source_data)

    merchants = source_data[2]

    assert set(df["merchant_key"]).issubset(
        set(merchants["merchant_key"])
    )


def test_device_ids_are_valid(source_data):
    df = make_transactions(source_data)

    devices = source_data[3]

    assert set(df["device_key"]).issubset(
        set(devices["device_key"])
    )


def test_geography_ids_are_valid(source_data):
    df = make_transactions(source_data)

    geography = source_data[4]

    assert set(df["geography_key"]).issubset(
        set(geography["geography_key"])
    )


def test_date_keys_are_valid(source_data):
    df = make_transactions(source_data)

    dates = source_data[5]

    assert set(df["date_key"]).issubset(
        set(dates["date_key"])
    )


def test_transaction_amounts_are_positive(source_data):
    df = make_transactions(source_data)

    assert (df["transaction_amount"] > 0).all()


def test_transaction_currency_is_gbp(source_data):
    df = make_transactions(source_data)

    assert (df["currency"] == "GBP").all()


def test_transaction_types_are_valid(source_data):
    df = make_transactions(source_data)

    assert set(df["transaction_type"]).issubset(
        set(TRANSACTION_TYPES)
    )


def test_transaction_channels_are_valid(source_data):
    df = make_transactions(source_data)

    assert set(df["transaction_channel"]).issubset(
        set(TRANSACTION_CHANNELS)
    )


def test_transaction_statuses_are_valid(source_data):
    df = make_transactions(source_data)

    assert set(df["transaction_status"]).issubset(
        set(TRANSACTION_STATUSES)
    )


def test_transaction_timestamps_are_valid(source_data):
    df = make_transactions(source_data)

    timestamps = pd.to_datetime(
        df["transaction_timestamp"]
    )

    assert timestamps.min() >= pd.Timestamp(
        START_DATE
    )

    assert timestamps.max() < (
        pd.Timestamp(END_DATE)
        + pd.Timedelta(days=1)
    )


def test_transaction_date_not_before_account_open_date(
    source_data,
):
    df = make_transactions(source_data)

    accounts = source_data[1]

    merged = df.merge(
        accounts[
            [
                "account_key",
                "account_open_date",
            ]
        ],
        on="account_key",
        how="left",
    )

    assert (
        pd.to_datetime(
            merged["transaction_timestamp"]
        ).dt.normalize()
        >= pd.to_datetime(
            merged["account_open_date"]
        ).dt.normalize()
    ).all()


def test_transaction_grain_is_one_row_per_transaction(
    source_data,
):
    df = make_transactions(source_data)

    assert len(df) == df["transaction_id"].nunique()


def test_transaction_generation_is_reproducible(
    source_data,
):
    df1 = make_transactions(
        source_data,
        count=500,
        seed=20260817,
    )

    df2 = make_transactions(
        source_data,
        count=500,
        seed=20260817,
    )

    pd.testing.assert_frame_equal(df1, df2)


def test_different_seed_changes_transactions(
    source_data,
):
    df1 = make_transactions(
        source_data,
        count=500,
        seed=20260817,
    )

    df2 = make_transactions(
        source_data,
        count=500,
        seed=20260818,
    )

    assert not df1.equals(df2)


def test_invalid_count_is_rejected(source_data):
    with pytest.raises(ValueError):
        make_transactions(
            source_data,
            count=0,
        )


def test_empty_customer_data_is_rejected(source_data):
    with pytest.raises(ValueError):
        generate_transactions(
            customers=pd.DataFrame(),
            accounts=source_data[1],
            merchants=source_data[2],
            devices=source_data[3],
            geography=source_data[4],
            dates=source_data[5],
            count=100,
            seed=20260817,
            start_date=START_DATE,
            end_date=END_DATE,
        )


def test_missing_required_column_is_rejected(source_data):
    customers = source_data[0].drop(
        columns=["customer_key"]
    )

    with pytest.raises(ValueError):
        generate_transactions(
            customers=customers,
            accounts=source_data[1],
            merchants=source_data[2],
            devices=source_data[3],
            geography=source_data[4],
            dates=source_data[5],
            count=100,
            seed=20260817,
            start_date=START_DATE,
            end_date=END_DATE,
        )
