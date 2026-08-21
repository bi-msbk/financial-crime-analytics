from __future__ import annotations

import sys
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_GENERATION_SRC = (
    PROJECT_ROOT / "03_Data_Generation" / "src"
)

QUALITY_SRC = (
    PROJECT_ROOT / "04_Data_Quality" / "src"
)

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
    / "v1.0"
)


def main() -> None:

    start = time.perf_counter()

    print("=" * 70)
    print("FINANCIAL CRIME ANALYTICS PLATFORM")
    print("PRODUCTION DATASET GENERATION")
    print("=" * 70)

    print("\nGenerating production dataset...")
    print("Customers:     50,000")
    print("Accounts:      65,000")
    print("Merchants:      5,000")
    print("Devices:       75,000")
    print("Transactions: 2,000,000")

    dataset = generate_dataset(
        customer_count=50_000,
        account_count=65_000,
        merchant_count=5_000,
        device_count=75_000,
        geography_count=100,
        transaction_count=2_000_000,
        seed=SEED,
    )

    generation_seconds = (
        time.perf_counter() - start
    )

    print(
        f"\nGeneration completed in "
        f"{generation_seconds:.2f} seconds"
    )

    print("\nDataset row counts:")
    print("-" * 45)

    for name, dataframe in dataset.items():
        print(
            f"{name:25s} {len(dataframe):>12,}"
        )

    print("\nRunning data quality gate...")

    quality_start = time.perf_counter()

    quality_result = run_quality_checks(dataset)

    quality_seconds = (
        time.perf_counter() - quality_start
    )

    print(
        f"\nQuality checks: "
        f"{quality_result['check_count']}"
    )

    print(
        f"Failed checks: "
        f"{quality_result['failed_count']}"
    )

    print(
        f"Quality status: "
        f"{'PASS' if quality_result['passed'] else 'FAIL'}"
    )

    print(
        f"Quality runtime: "
        f"{quality_seconds:.2f} seconds"
    )

    if not quality_result["passed"]:

        print("\nFAILED QUALITY CHECKS")
        print("-" * 45)

        for name, result in (
            quality_result["checks"].items()
        ):
            if not result["passed"]:
                print(
                    f"\n{name}:"
                )
                print(result)

        raise SystemExit(
            "Production quality gate failed."
        )

    print("\nExporting Parquet datasets...")

    export_start = time.perf_counter()

    paths = export_dataset(
        dataset=dataset,
        output_dir=OUTPUT_DIR,
        compression="snappy",
    )

    export_seconds = (
        time.perf_counter() - export_start
    )

    total_bytes = 0

    print("\nExported files:")
    print("-" * 70)

    for name, path in paths.items():

        size_bytes = path.stat().st_size
        total_bytes += size_bytes

        size_mb = (
            size_bytes / (1024 ** 2)
        )

        print(
            f"{name:25s}"
            f"{size_mb:>10.2f} MB"
        )

    total_mb = (
        total_bytes / (1024 ** 2)
    )

    print("\n" + "=" * 70)

    print(
        f"Total Parquet size: "
        f"{total_mb:.2f} MB"
    )

    print(
        f"Export time: "
        f"{export_seconds:.2f} seconds"
    )

    total_seconds = (
        time.perf_counter() - start
    )

    print(
        f"Total runtime: "
        f"{total_seconds:.2f} seconds"
    )

    print(
        f"\nOutput directory:"
        f"\n{OUTPUT_DIR}"
    )

    print("\nPRODUCTION DATASET READY")
    print("=" * 70)


if __name__ == "__main__":
    main()
