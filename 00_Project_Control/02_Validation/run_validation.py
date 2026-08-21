from pathlib import Path

from engine.config_loader import (
    ConfigurationError,
    load_all_configurations,
)

from engine.validator import (
    validate_project_configuration,
    validate_metric_configuration,
    validate_validation_configuration,
)


def main() -> int:

    project_root = Path(__file__).resolve().parents[2]

    try:
        configs = load_all_configurations(project_root)
    except ConfigurationError as exc:
        print(f"CONFIGURATION ERROR: {exc}")
        return 1

    results = []

    results.extend(
        validate_project_configuration(
            configs["project"]
        )
    )

    results.extend(
        validate_metric_configuration(
            configs["metrics"]
        )
    )

    results.extend(
        validate_validation_configuration(
            configs["validation"]
        )
    )

    print()
    print("=" * 70)
    print("PROJECT CONFIGURATION VALIDATION")
    print("=" * 70)

    passed = 0
    failed = 0

    for result in results:

        print(
            f"[{result.status}] "
            f"{result.rule_id}: "
            f"{result.message}"
        )

        if result.status == "PASS":
            passed += 1
        else:
            failed += 1

    print()
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed:
        print()
        print("CONFIGURATION VALIDATION FAILED.")
        return 1

    print()
    print("CONFIGURATION VALIDATION PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
