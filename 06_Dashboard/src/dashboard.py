from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPORT_DIR = (
    PROJECT_ROOT
    / "05_SQL_Analytics"
    / "reports"
)


def load_report(filename: str) -> pd.DataFrame:
    """
    Load an analytical CSV report.
    """
    path = REPORT_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Report not found: {path}"
        )

    result = pd.read_csv(path)

    if result.empty:
        raise ValueError(
            f"Report is empty: {path}"
        )

    return result


def build_executive_metrics() -> pd.DataFrame:
    """
    Build a presentation-friendly executive KPI table.
    """

    report = load_report(
        "executive_summary.csv"
    )

    row = report.iloc[0]

    metrics = [
        {
            "metric": "Transaction Count",
            "value": int(row["transaction_count"]),
        },
        {
            "metric": "Transaction Value",
            "value": float(
                row["total_transaction_value"]
            ),
        },
        {
            "metric": "Fraud Transactions",
            "value": int(
                row["fraud_transaction_count"]
            ),
        },
        {
            "metric": "Fraud Rate",
            "value": float(
                row["fraud_rate_pct"]
            ),
        },
        {
            "metric": "Total Fraud Loss",
            "value": float(
                row["total_fraud_loss"]
            ),
        },
        {
            "metric": "Detection Rate",
            "value": float(
                row["detection_rate_pct"]
            ),
        },
        {
            "metric": "Precision",
            "value": float(
                row["precision_pct"]
            ),
        },
        {
            "metric": "Open Cases",
            "value": int(
                row["open_cases"]
            ),
        },
    ]

    return pd.DataFrame(metrics)

def build_executive_dashboard(output_path):
    """
    Create an executive KPI dashboard PNG.
    """

    metrics = build_executive_metrics()

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.axis("off")

    ax.set_title(
        "Financial Crime Analytics Platform",
        fontsize=20,
        fontweight="bold",
        pad=30,
    )

    positions = [
        (0.05, 0.70),
        (0.35, 0.70),
        (0.65, 0.70),
        (0.05, 0.40),
        (0.35, 0.40),
        (0.65, 0.40),
        (0.05, 0.10),
        (0.35, 0.10),
    ]

    for index, (_, row) in enumerate(metrics.iterrows()):
        x, y = positions[index]

        metric = row["metric"]
        value = row["value"]

        if metric == "Transaction Count":
            display_value = f"{value:,.0f}"

        elif metric == "Transaction Value":
            display_value = f"Â£{value / 1_000_000:.1f}M"

        elif metric == "Fraud Transactions":
            display_value = f"{value:,.0f}"

        elif metric == "Fraud Rate":
            display_value = f"{value:.2f}%"

        elif metric == "Total Fraud Loss":
            display_value = f"Â£{value / 1_000_000:.2f}M"

        elif metric == "Detection Rate":
            display_value = f"{value:.2f}%"

        elif metric == "Precision":
            display_value = f"{value:.2f}%"

        elif metric == "Open Cases":
            display_value = f"{value:,.0f}"

        else:
            display_value = str(value)

        ax.text(
            x,
            y + 0.08,
            metric,
            transform=ax.transAxes,
            fontsize=11,
            fontweight="bold",
        )

        ax.text(
            x,
            y,
            display_value,
            transform=ax.transAxes,
            fontsize=22,
            fontweight="bold",
        )

    fig.text(
        0.05,
        0.02,
        "Synthetic production dataset | 2M transactions | 2024â€“2025",
        fontsize=9,
    )

    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(fig)

    return output_path
def build_fraud_scenario_chart(output_path):
    """
    Create fraud-loss-by-scenario chart PNG.
    """

    report = load_report("fraud_analysis.csv")

    report = report.sort_values(
        "fraud_loss",
        ascending=True,
    )

    fig, ax = plt.subplots(figsize=(11, 7))

    ax.barh(
        report["fraud_scenario"],
        report["fraud_loss"],
    )

    ax.set_title(
        "Fraud Loss by Scenario",
        fontsize=18,
        fontweight="bold",
    )

    ax.set_xlabel("Fraud Loss (Â£)")
    ax.set_ylabel("Fraud Scenario")

    ax.ticklabel_format(
        axis="x",
        style="plain",
    )

    for index, value in enumerate(report["fraud_loss"]):
        ax.text(
            value,
            index,
            f" Â£{value / 1_000_000:.2f}M",
            va="center",
            fontsize=9,
        )

    fig.tight_layout()

    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(fig)

    return output_path
def build_channel_risk_chart(output_path):
    """
    Create fraud-rate-by-channel chart.
    """

    report = load_report(
        "channel_transaction_type_risk.csv"
    )

    channel_report = (
        report[
            report["analysis_dimension"] == "Channel"
        ]
        .copy()
        .sort_values(
            "fraud_rate_pct",
            ascending=True,
        )
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    bars = ax.barh(
        channel_report["segment"],
        channel_report["fraud_rate_pct"],
    )

    ax.set_title(
        "Fraud Rate by Transaction Channel",
        fontsize=18,
        fontweight="bold",
    )

    ax.set_xlabel(
        "Fraud Rate (%)"
    )

    ax.set_ylabel(
        "Channel"
    )

    ax.set_xlim(
        0,
        channel_report["fraud_rate_pct"].max() * 1.20,
    )

    for bar, value in zip(
        bars,
        channel_report["fraud_rate_pct"],
    ):
        ax.text(
            value,
            bar.get_y() + bar.get_height() / 2,
            f" {value:.2f}%",
            va="center",
            fontsize=10,
        )

    fig.tight_layout()

    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(fig)

    return output_path

def build_channel_transaction_heatmap(output_path):
    """
    Create channel Ã— transaction-type fraud-rate heatmap.
    """

    report = load_report(
        "channel_transaction_risk.csv"
    )

    heatmap_data = report.pivot(
        index="channel",
        columns="transaction_type",
        values="fraud_rate_pct",
    )

    fig, ax = plt.subplots(
        figsize=(10, 7)
    )

    image = ax.imshow(
        heatmap_data.values,
        aspect="auto",
    )

    ax.set_title(
        "Fraud Rate: Channel Ã— Transaction Type",
        fontsize=18,
        fontweight="bold",
    )

    ax.set_xlabel(
        "Transaction Type"
    )

    ax.set_ylabel(
        "Channel"
    )

    ax.set_xticks(
        range(len(heatmap_data.columns))
    )

    ax.set_xticklabels(
        heatmap_data.columns,
        rotation=30,
        ha="right",
    )

    ax.set_yticks(
        range(len(heatmap_data.index))
    )

    ax.set_yticklabels(
        heatmap_data.index
    )

    for row in range(
        len(heatmap_data.index)
    ):
        for column in range(
            len(heatmap_data.columns)
        ):
            value = heatmap_data.iloc[
                row,
                column,
            ]

            if pd.notna(value):
                ax.text(
                    column,
                    row,
                    f"{value:.2f}%",
                    ha="center",
                    va="center",
                    fontsize=9,
                )

    colorbar = fig.colorbar(
        image,
        ax=ax,
    )

    colorbar.set_label(
        "Fraud Rate (%)"
    )

    fig.tight_layout()

    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(fig)

    return output_path

def build_customer_concentration_chart(output_path):
    """
    Create customer fraud-loss concentration chart.
    """

    report = load_report(
        "customer_concentration.csv"
    )

    report = report.copy()

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    bars = ax.bar(
        report["customer_segment"],
        report["fraud_loss_share_pct"],
    )

    ax.set_title(
        "Fraud Loss Concentration by Customer Segment",
        fontsize=18,
        fontweight="bold",
    )

    ax.set_xlabel(
        "Customer Segment"
    )

    ax.set_ylabel(
        "Share of Fraud Loss (%)"
    )

    ax.set_ylim(
        0,
        report["fraud_loss_share_pct"].max() * 1.25,
    )

    for bar, value in zip(
        bars,
        report["fraud_loss_share_pct"],
    ):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            f"{value:.2f}%",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    fig.tight_layout()

    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(fig)

    return output_path

def build_control_confusion_matrix(output_path):
    """
    Create control confusion matrix heatmap.
    """

    report = load_report(
        "control_confusion_matrix.csv"
    )

    row = report.iloc[0]

    matrix = pd.DataFrame(
        [
            [
                row["true_positive"],
                row["false_negative"],
            ],
            [
                row["false_positive"],
                row["true_negative"],
            ],
        ],
        index=[
            "Actual Fraud",
            "Actual Non-Fraud",
        ],
        columns=[
            "Alerted",
            "Not Alerted",
        ],
    )

    fig, ax = plt.subplots(
        figsize=(9, 7)
    )

    image = ax.imshow(
        matrix.values,
        aspect="auto",
    )

    ax.set_title(
        "Fraud Detection Control â€” Confusion Matrix",
        fontsize=18,
        fontweight="bold",
    )

    ax.set_xlabel(
        "Control Decision"
    )

    ax.set_ylabel(
        "Actual Classification"
    )

    ax.set_xticks(
        range(len(matrix.columns))
    )

    ax.set_xticklabels(
        matrix.columns
    )

    ax.set_yticks(
        range(len(matrix.index))
    )

    ax.set_yticklabels(
        matrix.index
    )

    for row_index in range(
        len(matrix.index)
    ):
        for column_index in range(
            len(matrix.columns)
        ):
            value = matrix.iloc[
                row_index,
                column_index,
            ]

            ax.text(
                column_index,
                row_index,
                f"{value:,.0f}",
                ha="center",
                va="center",
                fontsize=12,
                fontweight="bold",
            )

    colorbar = fig.colorbar(
        image,
        ax=ax,
    )

    colorbar.set_label(
        "Transaction Count"
    )

    fig.tight_layout()

    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(fig)

    return output_path

def build_rule_effectiveness_chart(output_path):
    """
    Create rule effectiveness chart showing precision by rule.
    """

    report = load_report(
        "rule_effectiveness.csv"
    )

    report = report.sort_values(
        "precision_pct",
        ascending=True,
    )

    fig, ax = plt.subplots(
        figsize=(11, 7)
    )

    ax.barh(
        report["rule_id"],
        report["precision_pct"],
    )

    ax.set_title(
        "Fraud Detection Rule Effectiveness",
        fontsize=18,
        fontweight="bold",
    )

    ax.set_xlabel(
        "Precision (%)"
    )

    ax.set_ylabel(
        "Detection Rule"
    )

    ax.set_xlim(
        0,
        100,
    )

    for index, value in enumerate(
        report["precision_pct"]
    ):
        ax.text(
            value + 1,
            index,
            f"{value:.2f}%",
            va="center",
            fontsize=10,
        )

    fig.tight_layout()

    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(fig)

    return output_path


def build_investigation_effectiveness_chart(output_path):
    """
    Create investigation effectiveness chart showing case status.
    """

    report = load_report(
        "investigation_effectiveness.csv"
    )

    row = report.iloc[0]

    closed_cases = float(
        row["closed_cases"]
    )

    open_cases = float(
        row["open_cases"]
    )

    labels = [
        "Closed Cases",
        "Open Cases",
    ]

    values = [
        closed_cases,
        open_cases,
    ]

    fig, ax = plt.subplots(
        figsize=(10, 7)
    )

    bars = ax.bar(
        labels,
        values,
    )

    ax.set_title(
        "Investigation Case Effectiveness",
        fontsize=18,
        fontweight="bold",
    )

    ax.set_ylabel(
        "Number of Cases"
    )

    for bar, value in zip(
        bars,
        values,
    ):
        ax.text(
            bar.get_x()
            + bar.get_width() / 2,
            value,
            f"{value:,.0f}",
            ha="center",
            va="bottom",
            fontsize=11,
        )

    ax.text(
        0.5,
        0.92,
        (
            f"Closure Rate: "
            f"{float(row['closure_rate_pct']):.2f}%"
            f" | Open Case Rate: "
            f"{float(row['open_case_rate_pct']):.2f}%"
        ),
        transform=ax.transAxes,
        ha="center",
        fontsize=11,
    )

    fig.tight_layout()

    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(fig)

    return output_path
