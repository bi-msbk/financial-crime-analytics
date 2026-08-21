from __future__ import annotations

import pandas as pd

from generators.customer import generate_customer
from generators.account import generate_accounts
from generators.merchant import generate_merchants
from generators.device import generate_devices
from generators.geography import generate_geography
from generators.date import generate_date
from generators.transaction import generate_transactions

from behaviour.customer_behaviour import (
    generate_customer_behaviour_profiles,
)

from fraud.fraud_simulation import simulate_fraud
from fraud.fraud_outcome import generate_fraud_outcomes

from controls.control_evaluation import evaluate_controls

from pipeline.investigation_simulation import (
    generate_investigation_cases,
)


REQUIRED_DATASETS = [
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
]


DEFAULT_START_DATE = "2024-01-01"
DEFAULT_END_DATE = "2025-12-31"


def generate_dataset(
    customer_count: int = 500,
    account_count: int = 650,
    merchant_count: int = 100,
    device_count: int = 750,
    geography_count: int = 50,
    transaction_count: int = 1000,
    seed: int = 20260817,
    start_date: str = DEFAULT_START_DATE,
    end_date: str = DEFAULT_END_DATE,
) -> dict[str, pd.DataFrame]:
    """
    Execute the complete synthetic financial-crime dataset pipeline.

    Generation order:

        dimensions
            â†“
        transactions
            â†“
        customer behaviour
            â†“
        fraud simulation
            â†“
        fraud outcomes
            â†“
        control evaluation
            â†“
        investigation cases

    Returns:
        Dictionary containing all generated datasets.
    """

    if customer_count <= 0:
        raise ValueError("customer_count must be greater than zero")

    if account_count <= 0:
        raise ValueError("account_count must be greater than zero")

    if merchant_count <= 0:
        raise ValueError("merchant_count must be greater than zero")

    if device_count <= 0:
        raise ValueError("device_count must be greater than zero")

    if geography_count <= 0:
        raise ValueError("geography_count must be greater than zero")

    if transaction_count <= 0:
        raise ValueError(
            "transaction_count must be greater than zero"
        )

    # ------------------------------------------------------------------
    # 1. Dimensions
    # ------------------------------------------------------------------

    geography = generate_geography(
        count=geography_count,
        seed=seed,
    )

    dates = generate_date(
        start_date=start_date,
        end_date=end_date,
    )

    customer = generate_customer(
        count=customer_count,
        seed=seed,
        start_date=start_date,
        end_date=end_date,
    )

    account = generate_accounts(
        customers=customer,
        count=account_count,
        seed=seed,
        start_date=start_date,
        end_date=end_date,
    )

    merchant = generate_merchants(
        count=merchant_count,
        seed=seed,
    )

    device = generate_devices(
        count=device_count,
        seed=seed,
        start_date=start_date,
        end_date=end_date,
    )

    # ------------------------------------------------------------------
    # 2. Transactions
    # ------------------------------------------------------------------

    transaction = generate_transactions(
        customers=customer,
        accounts=account,
        merchants=merchant,
        devices=device,
        geography=geography,
        dates=dates,
        count=transaction_count,
        seed=seed,
        start_date=start_date,
        end_date=end_date,
    )

    # ------------------------------------------------------------------
    # 3. Customer behavioural profile
    # ------------------------------------------------------------------

    customer_behaviour = generate_customer_behaviour_profiles(
        customers=customer,
        seed=seed,
    )

    # ------------------------------------------------------------------
    # 4. Fraud simulation
    # ------------------------------------------------------------------

    fraud_result = simulate_fraud(
    transactions=transaction,
    seed=seed,
    prevalence=0.015,
    )

    transaction = transaction.copy()

    transaction["fraud_flag"] = fraud_result["fraud_flag"].to_numpy()
    transaction["fraud_scenario"] = fraud_result["fraud_type"].to_numpy()
    transaction["fraud_type"] = fraud_result["fraud_type"].to_numpy()
    transaction["fraud_loss_amount"] = (
    fraud_result["fraud_loss_amount"].to_numpy()
    )

    # ------------------------------------------------------------------
    # 5. Fraud outcomes
    # ------------------------------------------------------------------

    fraud_outcome = generate_fraud_outcomes(
        transactions=transaction,
        seed=seed,
    )

    # ------------------------------------------------------------------
    # 6. Control evaluation
    # ------------------------------------------------------------------

    control_evaluation = evaluate_controls(
        transactions=transaction,
        seed=seed,
    )

    # ------------------------------------------------------------------
    # 7. Investigation simulation
    # ------------------------------------------------------------------

    investigation = generate_investigation_cases(
        transactions=transaction,
        alerts=control_evaluation,
        seed=seed,
    )

    return {
        "customer": customer,
        "account": account,
        "merchant": merchant,
        "device": device,
        "geography": geography,
        "date": dates,
        "transaction": transaction,
        "customer_behaviour": customer_behaviour,
        "fraud_outcome": fraud_outcome,
        "control_evaluation": control_evaluation,
        "investigation": investigation,
    }
from pathlib import Path


def export_dataset(
    dataset: dict[str, pd.DataFrame],
    output_dir: str | Path,
    compression: str = "snappy",
) -> dict[str, Path]:
    """
    Export generated datasets as Parquet files.

    One Parquet file is created per dataset.

    Returns:
        Dictionary mapping dataset names to output paths.
    """

    if dataset is None or not dataset:
        raise ValueError("dataset must contain at least one DataFrame")

    output_path = Path(output_dir)
    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    exported_paths: dict[str, Path] = {}

    for name, dataframe in dataset.items():

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(
                f"dataset['{name}'] must be a pandas DataFrame"
            )

        file_path = output_path / f"{name}.parquet"

        dataframe.to_parquet(
            file_path,
            index=False,
            compression=compression,
        )

        exported_paths[name] = file_path

    return exported_paths
