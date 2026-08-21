from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

QUALITY_SRC = (
    PROJECT_ROOT / "04_Data_Quality" / "src"
)

if str(QUALITY_SRC) not in sys.path:
    sys.path.insert(0, str(QUALITY_SRC))

from quality_checks import run_quality_checks


DATA_DIR = (
    PROJECT_ROOT
    / "03_Data_Generation"
    / "output"
    / "v1.0"
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


def load_production_dataset():
    datasets = {}

    for name in REQUIRED_DATASETS:
        path = DATA_DIR / f"{name}.parquet"

        assert path.exists(), (
            f"Missing production file: {path}"
        )

        datasets[name] = pd.read_parquet(path)

    return datasets


def test_all_production_parquet_files_exist():
    for name in REQUIRED_DATASETS:
        path = DATA_DIR / f"{name}.parquet"

        assert path.exists()


def test_production_transaction_count():
    transactions = pd.read_parquet(
        DATA_DIR / "transaction.parquet"
    )

    assert len(transactions) == 2_000_000


def test_production_fraud_count():
    fraud_outcomes = pd.read_parquet(
        DATA_DIR / "fraud_outcome.parquet"
    )

    assert len(fraud_outcomes) == 30_000


def test_production_parquet_quality_gate():
    datasets = load_production_dataset()

    result = run_quality_checks(
        datasets
    )

    assert result["passed"] is True
    assert result["failed_count"] == 0


def test_production_transaction_ids_are_unique():
    transactions = pd.read_parquet(
        DATA_DIR / "transaction.parquet"
    )

    assert transactions[
        "transaction_id"
    ].is_unique


def test_production_fraud_outcome_ids_are_unique():
    outcomes = pd.read_parquet(
        DATA_DIR / "fraud_outcome.parquet"
    )

    assert outcomes[
        "fraud_outcome_id"
    ].is_unique
