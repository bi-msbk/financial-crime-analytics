from pathlib import Path

from engine.config_loader import load_all_configurations
from engine.validator import (
    validate_project_configuration,
    validate_metric_configuration,
    validate_validation_configuration,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def test_all_configurations_load():
    configs = load_all_configurations(PROJECT_ROOT)

    assert "project" in configs
    assert "metrics" in configs
    assert "validation" in configs


def test_project_configuration_is_valid():
    configs = load_all_configurations(PROJECT_ROOT)

    results = validate_project_configuration(
        configs["project"]
    )

    failures = [
        result
        for result in results
        if result.status == "FAIL"
    ]

    assert not failures


def test_metric_configuration_is_valid():
    configs = load_all_configurations(PROJECT_ROOT)

    results = validate_metric_configuration(
        configs["metrics"]
    )

    failures = [
        result
        for result in results
        if result.status == "FAIL"
    ]

    assert not failures


def test_validation_configuration_is_valid():
    configs = load_all_configurations(PROJECT_ROOT)

    results = validate_validation_configuration(
        configs["validation"]
    )

    failures = [
        result
        for result in results
        if result.status == "FAIL"
    ]

    assert not failures


def test_required_tables_are_defined():
    configs = load_all_configurations(PROJECT_ROOT)

    validation = configs["validation"]

    dimensions = validation["required_tables"]["dimensions"]
    facts = validation["required_tables"]["facts"]

    assert "dim_customer" in dimensions
    assert "dim_account" in dimensions
    assert "fact_transaction" in facts
    assert "fact_fraud_alert" in facts
    assert "fact_investigation_case" in facts


def test_required_grains_are_defined():
    configs = load_all_configurations(PROJECT_ROOT)

    validation = configs["validation"]

    grain_rules = validation["grain"]

    tables = {
        rule["table"]
        for rule in grain_rules
    }

    assert "dim_customer" in tables
    assert "dim_account" in tables
    assert "fact_transaction" in tables
    assert "fact_fraud_alert" in tables
    assert "fact_investigation_case" in tables


def test_required_relationships_are_defined():
    configs = load_all_configurations(PROJECT_ROOT)

    validation = configs["validation"]

    relationships = validation["relationships"]

    assert len(relationships) > 0

    parent_child_pairs = {
        (
            relationship["parent_table"],
            relationship["child_table"],
        )
        for relationship in relationships
    }

    assert (
        "dim_customer",
        "dim_account",
    ) in parent_child_pairs

    assert (
        "dim_account",
        "fact_transaction",
    ) in parent_child_pairs

    assert (
        "fact_transaction",
        "fact_fraud_alert",
    ) in parent_child_pairs
