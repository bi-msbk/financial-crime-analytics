from __future__ import annotations

from typing import Any

import pandas as pd


def check_required_columns(
    dataframe: pd.DataFrame,
    required_columns: list[str],
) -> dict[str, Any]:
    missing = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    return {
        "passed": len(missing) == 0,
        "missing_columns": missing,
    }


def check_nulls(
    dataframe: pd.DataFrame,
    columns: list[str],
) -> dict[str, Any]:
    null_counts = {
        column: int(dataframe[column].isna().sum())
        for column in columns
        if column in dataframe.columns
    }

    return {
        "passed": all(
            count == 0
            for count in null_counts.values()
        ),
        "null_counts": null_counts,
    }


def check_unique(
    dataframe: pd.DataFrame,
    column: str,
) -> dict[str, Any]:
    if column not in dataframe.columns:
        return {
            "passed": False,
            "reason": f"Missing column: {column}",
        }

    return {
        "passed": bool(dataframe[column].is_unique),
        "duplicate_count": int(
            dataframe[column].duplicated().sum()
        ),
    }


def check_positive(
    dataframe: pd.DataFrame,
    column: str,
) -> dict[str, Any]:
    if column not in dataframe.columns:
        return {
            "passed": False,
            "reason": f"Missing column: {column}",
        }

    invalid_count = int(
        (dataframe[column] <= 0).sum()
    )

    return {
        "passed": invalid_count == 0,
        "invalid_count": invalid_count,
    }


def check_allowed_values(
    dataframe: pd.DataFrame,
    column: str,
    allowed_values: set[Any],
) -> dict[str, Any]:
    if column not in dataframe.columns:
        return {
            "passed": False,
            "reason": f"Missing column: {column}",
        }

    invalid_values = sorted(
        set(dataframe[column].dropna())
        - allowed_values
    )

    return {
        "passed": len(invalid_values) == 0,
        "invalid_values": invalid_values,
    }


def check_foreign_key(
    child: pd.DataFrame,
    child_column: str,
    parent: pd.DataFrame,
    parent_column: str,
) -> dict[str, Any]:
    if child_column not in child.columns:
        return {
            "passed": False,
            "reason": f"Missing child column: {child_column}",
        }

    if parent_column not in parent.columns:
        return {
            "passed": False,
            "reason": f"Missing parent column: {parent_column}",
        }

    valid_values = set(
        parent[parent_column].dropna()
    )

    invalid_count = int(
        (~child[child_column].isin(valid_values)).sum()
    )

    return {
        "passed": invalid_count == 0,
        "invalid_count": invalid_count,
    }


def check_non_fraud_zero_loss(
    transactions: pd.DataFrame,
) -> dict[str, Any]:
    required = {
        "fraud_flag",
        "fraud_loss_amount",
    }

    missing = required - set(transactions.columns)

    if missing:
        return {
            "passed": False,
            "reason": f"Missing columns: {sorted(missing)}",
        }

    non_fraud = transactions[
        ~transactions["fraud_flag"].astype(bool)
    ]

    invalid_count = int(
        (non_fraud["fraud_loss_amount"] != 0).sum()
    )

    return {
        "passed": invalid_count == 0,
        "invalid_count": invalid_count,
    }


def check_fraud_loss_not_exceeding_transaction(
    transactions: pd.DataFrame,
) -> dict[str, Any]:
    required = {
        "fraud_flag",
        "transaction_amount",
        "fraud_loss_amount",
    }

    missing = required - set(transactions.columns)

    if missing:
        return {
            "passed": False,
            "reason": f"Missing columns: {sorted(missing)}",
        }

    fraud = transactions[
        transactions["fraud_flag"].astype(bool)
    ]

    invalid_count = int(
        (
            fraud["fraud_loss_amount"]
            > fraud["transaction_amount"]
        ).sum()
    )

    return {
        "passed": invalid_count == 0,
        "invalid_count": invalid_count,
    }


def run_quality_checks(
    datasets: dict[str, pd.DataFrame],
) -> dict[str, Any]:
    """
    Run the core financial-crime dataset quality checks.

    Returns a structured quality report.
    """

    required_datasets = {
        "customer",
        "account",
        "merchant",
        "device",
        "geography",
        "date",
        "transaction",
        "fraud_outcome",
        "control_evaluation",
        "investigation",
    }

    missing_datasets = sorted(
        required_datasets - set(datasets.keys())
    )

    if missing_datasets:
        raise ValueError(
            f"Missing datasets: {missing_datasets}"
        )

    customer = datasets["customer"]
    account = datasets["account"]
    merchant = datasets["merchant"]
    device = datasets["device"]
    geography = datasets["geography"]
    dates = datasets["date"]
    transaction = datasets["transaction"]
    fraud_outcome = datasets["fraud_outcome"]
    controls = datasets["control_evaluation"]
    investigation = datasets["investigation"]

    checks: dict[str, Any] = {}

    checks["customer_key_unique"] = check_unique(
        customer,
        "customer_key",
    )

    checks["customer_id_unique"] = check_unique(
        customer,
        "customer_id",
    )

    checks["account_key_unique"] = check_unique(
        account,
        "account_key",
    )

    checks["merchant_key_unique"] = check_unique(
        merchant,
        "merchant_key",
    )

    checks["device_key_unique"] = check_unique(
        device,
        "device_key",
    )

    checks["geography_key_unique"] = check_unique(
        geography,
        "geography_key",
    )

    checks["transaction_id_unique"] = check_unique(
        transaction,
        "transaction_id",
    )

    checks["transaction_amount_positive"] = check_positive(
        transaction,
        "transaction_amount",
    )

    checks["transaction_customer_fk"] = check_foreign_key(
        transaction,
        "customer_key",
        customer,
        "customer_key",
    )

    checks["transaction_account_fk"] = check_foreign_key(
        transaction,
        "account_key",
        account,
        "account_key",
    )

    checks["transaction_merchant_fk"] = check_foreign_key(
        transaction,
        "merchant_key",
        merchant,
        "merchant_key",
    )

    checks["transaction_device_fk"] = check_foreign_key(
        transaction,
        "device_key",
        device,
        "device_key",
    )

    checks["transaction_geography_fk"] = check_foreign_key(
        transaction,
        "geography_key",
        geography,
        "geography_key",
    )

    checks["transaction_date_fk"] = check_foreign_key(
        transaction,
        "date_key",
        dates,
        "date_key",
    )

    checks["fraud_outcome_transaction_fk"] = check_foreign_key(
        fraud_outcome,
        "transaction_id",
        transaction,
        "transaction_id",
    )

    checks["control_transaction_fk"] = check_foreign_key(
        controls,
        "transaction_id",
        transaction,
        "transaction_id",
    )

    checks["investigation_alert_fk"] = check_foreign_key(
        investigation,
        "alert_id",
        controls,
        "alert_id",
    )

    checks["non_fraud_zero_loss"] = (
        check_non_fraud_zero_loss(transaction)
    )

    checks["fraud_loss_valid"] = (
        check_fraud_loss_not_exceeding_transaction(
            transaction
        )
    )

    passed = all(
        result["passed"]
        for result in checks.values()
    )

    return {
        "passed": passed,
        "check_count": len(checks),
        "failed_count": sum(
            not result["passed"]
            for result in checks.values()
        ),
        "checks": checks,
    }
