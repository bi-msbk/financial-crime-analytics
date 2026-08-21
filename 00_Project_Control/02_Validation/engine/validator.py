from __future__ import annotations

from typing import Any


class ValidationResult:
    def __init__(
        self,
        rule_id: str,
        status: str,
        message: str,
        severity: str = "critical",
    ) -> None:
        self.rule_id = rule_id
        self.status = status
        self.message = message
        self.severity = severity

    def as_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
        }


def validate_required_sections(
    config: dict[str, Any],
    required_sections: list[str],
) -> list[ValidationResult]:

    results: list[ValidationResult] = []

    for section in required_sections:
        if section in config:
            results.append(
                ValidationResult(
                    rule_id=f"CFG-SECTION-{section}",
                    status="PASS",
                    severity="critical",
                    message=f"Required section '{section}' exists.",
                )
            )
        else:
            results.append(
                ValidationResult(
                    rule_id=f"CFG-SECTION-{section}",
                    status="FAIL",
                    severity="critical",
                    message=f"Required section '{section}' is missing.",
                )
            )

    return results


def validate_project_configuration(
    project_config: dict[str, Any],
) -> list[ValidationResult]:

    required_sections = [
        "project",
        "governance",
        "lifecycle",
        "entities",
        "analytical_tables",
        "grain",
        "relationships",
        "fraud",
        "data_quality",
        "validation",
        "approval",
    ]

    return validate_required_sections(
        project_config,
        required_sections,
    )


def validate_metric_configuration(
    metric_config: dict[str, Any],
) -> list[ValidationResult]:

    results: list[ValidationResult] = []

    metrics = metric_config.get("metrics")

    if not isinstance(metrics, dict):
        results.append(
            ValidationResult(
                rule_id="CFG-METRIC-001",
                status="FAIL",
                severity="critical",
                message="'metrics' must be a mapping.",
            )
        )
        return results

    if not metrics:
        results.append(
            ValidationResult(
                rule_id="CFG-METRIC-002",
                status="FAIL",
                severity="critical",
                message="No metric definitions were found.",
            )
        )
        return results

    for metric_id, definition in metrics.items():

        if not isinstance(definition, dict):
            results.append(
                ValidationResult(
                    rule_id=f"CFG-METRIC-{metric_id}",
                    status="FAIL",
                    severity="critical",
                    message=f"{metric_id} must contain a mapping.",
                )
            )
            continue

        required_fields = [
            "name",
            "grain",
            "source_table",
            "measure_type",
            "calculation",
        ]

        missing = [
            field
            for field in required_fields
            if field not in definition
        ]

        if missing:
            results.append(
                ValidationResult(
                    rule_id=f"CFG-METRIC-{metric_id}",
                    status="FAIL",
                    severity="critical",
                    message=(
                        f"{metric_id} is missing required fields: "
                        f"{', '.join(missing)}"
                    ),
                )
            )
        else:
            results.append(
                ValidationResult(
                    rule_id=f"CFG-METRIC-{metric_id}",
                    status="PASS",
                    severity="critical",
                    message=f"{metric_id} is structurally valid.",
                )
            )

    return results


def validate_validation_configuration(
    validation_config: dict[str, Any],
) -> list[ValidationResult]:

    required_sections = [
        "governance",
        "thresholds",
        "required_tables",
        "primary_keys",
        "required_fields",
        "relationships",
        "grain",
        "domain_rules",
        "temporal_rules",
        "fraud_rules",
        "control_rules",
        "investigation_rules",
        "behavioural_rules",
        "reproducibility",
        "release_gates",
        "overall_status",
    ]

    return validate_required_sections(
        validation_config,
        required_sections,
    )
