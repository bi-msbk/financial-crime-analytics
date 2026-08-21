from pathlib import Path

from src.dashboard import (
    build_executive_dashboard,
    build_fraud_scenario_chart,
    build_channel_risk_chart,
    build_channel_transaction_heatmap,
    build_customer_concentration_chart,
    build_control_confusion_matrix,
    build_rule_effectiveness_chart,
    build_investigation_effectiveness_chart,
)

(
    "Rule effectiveness",
    build_rule_effectiveness_chart,
    "rule_effectiveness.png",
),
(
    "Investigation effectiveness",
    build_investigation_effectiveness_chart,
    "investigation_effectiveness.png",
),

PROJECT_ROOT = Path(__file__).resolve().parent

OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def main():
    print("=" * 70)
    print("FINANCIAL CRIME ANALYTICS PLATFORM")
    print("DASHBOARD VISUAL GENERATION")
    print("=" * 70)

    charts = [
    (
        "Executive dashboard",
        build_executive_dashboard,
        "executive_dashboard.png",
    ),
    (
        "Fraud scenarios",
        build_fraud_scenario_chart,
        "fraud_scenarios.png",
    ),
    (
        "Channel risk",
        build_channel_risk_chart,
        "channel_risk.png",
    ),
    (
        "Channel Ã— transaction type",
        build_channel_transaction_heatmap,
        "channel_transaction_heatmap.png",
    ),
    (
        "Customer concentration",
        build_customer_concentration_chart,
        "customer_concentration.png",
    ),
    (
        "Control confusion matrix",
        build_control_confusion_matrix,
        "control_confusion_matrix.png",
    ),
    (
        "Rule effectiveness",
        build_rule_effectiveness_chart,
        "rule_effectiveness.png",
    ),
    (
        "Investigation effectiveness",
        build_investigation_effectiveness_chart,
        "investigation_effectiveness.png",
    ),
]

    print()
    print("Generating visuals...")
    print("-" * 70)

    generated_files = []

    for name, builder, filename in charts:
        output_path = OUTPUT_DIR / filename

        result = builder(output_path)

        generated_files.append(result)

        print(
            f"{name:<35} {result.name}"
        )

    print()
    print("Generated files:")
    print("-" * 70)

    for path in generated_files:
        print(
            f"{path.name:<35} "
            f"{path.stat().st_size / 1024:.1f} KB"
        )

    print()
    print(
        f"Output directory: {OUTPUT_DIR}"
    )

    print()
    print("Dashboard generation completed.")
    print("=" * 70)


if __name__ == "__main__":
    main()
