from __future__ import annotations

import pandas as pd
import pytest

from pipeline.generate_dataset import (
    export_dataset,
)


def test_export_dataset_creates_parquet_files(tmp_path):
    dataset = {
        "customer": pd.DataFrame(
            {
                "customer_key": [1, 2],
                "customer_id": ["CUST000001", "CUST000002"],
            }
        ),
        "transaction": pd.DataFrame(
            {
                "transaction_key": [1, 2],
                "transaction_id": ["TXN00000001", "TXN00000002"],
            }
        ),
    }

    paths = export_dataset(
        dataset=dataset,
        output_dir=tmp_path,
    )

    assert set(paths.keys()) == {
        "customer",
        "transaction",
    }

    assert paths["customer"].exists()
    assert paths["transaction"].exists()

    assert paths["customer"].suffix == ".parquet"
    assert paths["transaction"].suffix == ".parquet"


def test_exported_parquet_can_be_read(tmp_path):
    source = pd.DataFrame(
        {
            "customer_key": [1, 2, 3],
            "customer_id": [
                "CUST000001",
                "CUST000002",
                "CUST000003",
            ],
        }
    )

    export_dataset(
        dataset={"customer": source},
        output_dir=tmp_path,
    )

    loaded = pd.read_parquet(
        tmp_path / "customer.parquet"
    )

    pd.testing.assert_frame_equal(
        source,
        loaded,
    )


def test_export_dataset_creates_output_directory(tmp_path):
    output_dir = tmp_path / "nested" / "data"

    dataset = {
        "customer": pd.DataFrame(
            {"customer_key": [1]}
        )
    }

    export_dataset(
        dataset=dataset,
        output_dir=output_dir,
    )

    assert output_dir.exists()
    assert (output_dir / "customer.parquet").exists()


def test_empty_dataset_is_rejected(tmp_path):
    with pytest.raises(ValueError):
        export_dataset(
            dataset={},
            output_dir=tmp_path,
        )


def test_non_dataframe_is_rejected(tmp_path):
    with pytest.raises(TypeError):
        export_dataset(
            dataset={
                "customer": ["not", "a", "dataframe"]
            },
            output_dir=tmp_path,
        )
