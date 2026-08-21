from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


QUALITY_SRC = (
    Path(__file__).resolve().parents[1] / "src"
)

if str(QUALITY_SRC) not in sys.path:
    sys.path.insert(0, str(QUALITY_SRC))


from quality_checks import (
    check_allowed_values,
    check_foreign_key,
    check_nulls,
    check_positive,
    check_required_columns,
    check_unique,
    run_quality_checks,
)


def test_required_columns_pass():
    df = pd.DataFrame(
        {
            "customer_id": ["C1"],
            "customer_key": [1],
        }
    )

    result = check_required_columns(
        df,
        ["customer_id", "customer_key"],
    )

    assert result["passed"] is True
    assert result["missing_columns"] == []


def test_required_columns_fail():
    df = pd.DataFrame(
        {"customer_id": ["C1"]}
    )

    result = check_required_columns(
        df,
        ["customer_id", "customer_key"],
    )

    assert result["passed"] is False
    assert result["missing_columns"] == [
        "customer_key"
    ]


def test_null_check_passes():
    df = pd.DataFrame(
        {"id": [1, 2, 3]}
    )

    result = check_nulls(
        df,
        ["id"],
    )

    assert result["passed"] is True


def test_null_check_fails():
    df = pd.DataFrame(
        {"id": [1, None, 3]}
    )

    result = check_nulls(
        df,
        ["id"],
    )

    assert result["passed"] is False
    assert result["null_counts"]["id"] == 1


def test_unique_check_passes():
    df = pd.DataFrame(
        {"id": [1, 2, 3]}
    )

    result = check_unique(
        df,
        "id",
    )

    assert result["passed"] is True


def test_unique_check_fails():
    df = pd.DataFrame(
        {"id": [1, 1, 3]}
    )

    result = check_unique(
        df,
        "id",
    )

    assert result["passed"] is False
    assert result["duplicate_count"] == 1


def test_positive_check_passes():
    df = pd.DataFrame(
        {"amount": [10.0, 20.0]}
    )

    result = check_positive(
        df,
        "amount",
    )

    assert result["passed"] is True


def test_positive_check_fails():
    df = pd.DataFrame(
        {"amount": [10.0, 0.0, -5.0]}
    )

    result = check_positive(
        df,
        "amount",
    )

    assert result["passed"] is False
    assert result["invalid_count"] == 2


def test_allowed_values_pass():
    df = pd.DataFrame(
        {"status": ["Active", "Closed"]}
    )

    result = check_allowed_values(
        df,
        "status",
        {"Active", "Closed"},
    )

    assert result["passed"] is True


def test_allowed_values_fail():
    df = pd.DataFrame(
        {"status": ["Active", "Unknown"]}
    )

    result = check_allowed_values(
        df,
        "status",
        {"Active", "Closed"},
    )

    assert result["passed"] is False
    assert result["invalid_values"] == ["Unknown"]


def test_foreign_key_passes():
    parent = pd.DataFrame(
        {"id": [1, 2, 3]}
    )

    child = pd.DataFrame(
        {"parent_id": [1, 2, 3]}
    )

    result = check_foreign_key(
        child,
        "parent_id",
        parent,
        "id",
    )

    assert result["passed"] is True


def test_foreign_key_fails():
    parent = pd.DataFrame(
        {"id": [1, 2, 3]}
    )

    child = pd.DataFrame(
        {"parent_id": [1, 2, 99]}
    )

    result = check_foreign_key(
        child,
        "parent_id",
        parent,
        "id",
    )

    assert result["passed"] is False
    assert result["invalid_count"] == 1


def test_full_quality_check_passes():
    datasets = {
        "customer": pd.DataFrame(
            {
                "customer_key": [1],
                "customer_id": ["C1"],
            }
        ),
        "account": pd.DataFrame(
            {
                "account_key": [1],
                "customer_key": [1],
            }
        ),
        "merchant": pd.DataFrame(
            {"merchant_key": [1]}
        ),
        "device": pd.DataFrame(
            {"device_key": [1]}
        ),
        "geography": pd.DataFrame(
            {"geography_key": [1]}
        ),
        "date": pd.DataFrame(
            {"date_key": [20240101]}
        ),
        "transaction": pd.DataFrame(
            {
                "transaction_id": ["T1"],
                "customer_key": [1],
                "account_key": [1],
                "merchant_key": [1],
                "device_key": [1],
                "geography_key": [1],
                "date_key": [20240101],
                "transaction_amount": [100.0],
                "fraud_flag": [False],
                "fraud_loss_amount": [0.0],
            }
        ),
        "fraud_outcome": pd.DataFrame(
            {
                "transaction_id": pd.Series(
                    dtype="object"
                )
            }
        ),
        "control_evaluation": pd.DataFrame(
            {
                "transaction_id": ["T1"],
                "alert_id": ["A1"],
            }
        ),
        "investigation": pd.DataFrame(
            {
                "alert_id": ["A1"],
            }
        ),
    }

    result = run_quality_checks(datasets)

    assert result["passed"] is True
    assert result["failed_count"] == 0
