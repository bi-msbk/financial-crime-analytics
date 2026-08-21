from __future__ import annotations

import sys
import time
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_GENERATION_SRC = PROJECT_ROOT / "03_Data_Generation" / "src"
QUALITY_SRC = PROJECT_ROOT / "04_Data_Quality" / "src"

sys.path.insert(0, str(DATA_GENERATION_SRC))
sys.path.insert(0, str(QUALITY_SRC))


from pipeline.generate_dataset import (  # noqa: E402
    generate_dataset,
    export_dataset,
)

from quality_checks import run_quality_checks  # noqa: E402


SEED = 20260817

OUTPUT_DIR = (
    PROJECT_ROOT
    / "03_Data_Generation"
    / "output"
    / "smoke"
)


def main() -> None:
    start = time.perf_counter()

    print("Generating 10,000 transaction smoke dataset...")

    dataset = generate_dataset(
        customer_count=2_500,
        account_count=3_000,
        merchant_count=250,
        device_count=3_500,
        geography_count=50,
        transaction_count=10_000,
        seed=SEED,
    )

    generation_seconds = time.perf_counter() - start

    print(
        f"Generation completed in "
        f"{generation_seconds:.2f} seconds"
    )

    print("\nDataset row counts:")

    for name, dataframe in dataset.items():
        print(
            f"{name:25s} "
            f"{len(dataframe):,}"
        )

    quality_start = time.perf_counter()

    quality_result = run_quality_checks(dataset)

    quality_seconds = time.perf_counter() - quality_start

    print("\nQuality result:")
    print(
        f"Passed: {quality_result['passed']}"
    )
    print(
        f"Checks: {quality_result['check_count']}"
    )
    print(
        f"Failed: {quality_result['failed_count']}"
    )
    print(
        f"Quality check time: "
        f"{quality_seconds:.2f} seconds"
    )

    if not quality_result["passed"]:
        print("\nFailed checks:")

        for name, result in quality_result["checks"].items():
            if not result["passed"]:
                print(
                    f" - {name}: {result}"
                )

        raise SystemExit(
            "Quality gate failed."
        )

    export_start = time.perf_counter()

    paths = export_dataset(
        dataset=dataset,
        output_dir=OUTPUT_DIR,
    )

    export_seconds = time.perf_counter() - export_start

    print("\nExported Parquet files:")

    total_bytes = 0

    for name, path in paths.items():
        size_bytes = path.stat().st_size
        total_bytes += size_bytes

        print(
            f"{name:25s} "
            f"{size_bytes / (1024 ** 2):,.2f} MB "
            f"{path}"
        )

    print(
        f"\nTotal Parquet size: "
        f"{total_bytes / (1024 ** 2):,.2f} MB"
    )

    print(
        f"Export time: "
        f"{export_seconds:.2f} seconds"
    )

    total_seconds = time.perf_counter() - start

    print(
        f"\nTotal smoke-test time: "
        f"{total_seconds:.2f} seconds"
    )

    print("\nSmoke test completed successfully.")


if __name__ == "__main__":
    main()
