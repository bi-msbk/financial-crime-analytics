from pathlib import Path

import pandas as pd

from dashboard import (
    REPORT_DIR,
    load_report,
    build_executive_metrics,
)


def test_report_directory_exists():
    assert REPORT_DIR.exists()


def test_load_report_returns_dataframe():
    result = load_report("executive_summary.csv")

    assert isinstance(result, pd.DataFrame)
    assert not result.empty


def test_executive_summary_has_expected_metrics():
    result = build_executive_metrics()

    expected_columns = {
        "metric",
        "value",
    }

    assert expected_columns.issubset(result.columns)


def test_executive_summary_has_transaction_count():
    result = build_executive_metrics()

    transaction_row = result.loc[
        result["metric"] == "Transaction Count"
    ]

    assert not transaction_row.empty
    assert transaction_row.iloc[0]["value"] == 2_000_000


def test_executive_summary_has_fraud_rate():
    result = build_executive_metrics()

    fraud_rate_row = result.loc[
        result["metric"] == "Fraud Rate"
    ]

    assert not fraud_rate_row.empty
    assert fraud_rate_row.iloc[0]["value"] == 1.5

def test_build_executive_dashboard_creates_png(tmp_path):
    output_path = tmp_path / "executive_dashboard.png"

    from dashboard import build_executive_dashboard

    result = build_executive_dashboard(output_path)

    assert result == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_build_fraud_scenario_chart_creates_png(tmp_path):
    output_path = tmp_path / "fraud_scenarios.png"

    from dashboard import build_fraud_scenario_chart

    result = build_fraud_scenario_chart(output_path)

    assert result == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0

def test_build_channel_risk_chart_creates_png(tmp_path):
    output_path = tmp_path / "channel_risk.png"

    from dashboard import build_channel_risk_chart

    result = build_channel_risk_chart(output_path)

    assert result == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_build_channel_transaction_heatmap_creates_png(tmp_path):
    output_path = tmp_path / "channel_transaction_heatmap.png"

    from dashboard import build_channel_transaction_heatmap

    result = build_channel_transaction_heatmap(output_path)

    assert result == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0

def test_build_customer_concentration_chart_creates_png(tmp_path):
    output_path = tmp_path / "customer_concentration.png"

    from dashboard import build_customer_concentration_chart

    result = build_customer_concentration_chart(output_path)

    assert result == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_build_control_confusion_matrix_creates_png(tmp_path):
    output_path = tmp_path / "control_confusion_matrix.png"

    from dashboard import build_control_confusion_matrix

    result = build_control_confusion_matrix(output_path)

    assert result == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0

def test_build_rule_effectiveness_chart_creates_png(tmp_path):
    output_path = tmp_path / "rule_effectiveness.png"

    from dashboard import build_rule_effectiveness_chart

    result = build_rule_effectiveness_chart(output_path)

    assert result == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_build_investigation_effectiveness_chart_creates_png(tmp_path):
    output_path = tmp_path / "investigation_effectiveness.png"

    from dashboard import build_investigation_effectiveness_chart

    result = build_investigation_effectiveness_chart(output_path)

    assert result == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0

def build_rule_effectiveness_chart(output_path):
    """
    Create rule effectiveness chart showing precision by rule.
    """

    report = load_report("rule_effectiveness.csv")

    report = report.sort_values(
        "precision_pct",
        ascending=True,
    )

    fig, ax = plt.subplots(figsize=(11, 7))

    ax.barh(
        report["rule_id"],
        report["precision_pct"],
    )

    ax.set_title(
        "Fraud Detection Rule Effectiveness",
        fontsize=18,
        fontweight="bold",
    )

    ax.set_xlabel("Precision (%)")
    ax.set_ylabel("Detection Rule")

    ax.set_xlim(0, 100)

    for index, value in enumerate(report["precision_pct"]):
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

    report = load_report("investigation_effectiveness.csv")

    closed_cases = float(report.loc[0, "closed_cases"])
    open_cases = float(report.loc[0, "open_cases"])

    labels = [
        "Closed Cases",
        "Open Cases",
    ]

    values = [
        closed_cases,
        open_cases,
    ]

    fig, ax = plt.subplots(figsize=(10, 7))

    bars = ax.bar(
        labels,
        values,
    )

    ax.set_title(
        "Investigation Case Effectiveness",
        fontsize=18,
        fontweight="bold",
    )

    ax.set_ylabel("Number of Cases")

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            f"{value:,.0f}",
            ha="center",
            va="bottom",
            fontsize=11,
        )

    ax.text(
        0.5,
        0.92,
        f"Closure Rate: {float(report.loc[0, 'closure_rate_pct']):.2f}%"
        f" | Open Case Rate: {float(report.loc[0, 'open_case_rate_pct']):.2f}%",
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
