from __future__ import annotations

import pandas as pd
import pytest

from src.generators.fraud_rule import (
    REQUIRED_COLUMNS,
    RULE_CATEGORIES,
    RULE_STATUSES,
    generate_fraud_rules,
)


def test_fraud_rule_returns_dataframe():
    df = generate_fraud_rules(count=8)

    assert isinstance(df, pd.DataFrame)


def test_fraud_rule_has_required_columns():
    df = generate_fraud_rules(count=8)

    assert list(df.columns) == REQUIRED_COLUMNS


def test_fraud_rule_has_expected_row_count():
    df = generate_fraud_rules(count=8)

    assert len(df) == 8


def test_fraud_rule_keys_are_unique():
    df = generate_fraud_rules(count=8)

    assert df["fraud_rule_key"].is_unique


def test_rule_identifiers_are_unique():
    df = generate_fraud_rules(count=8)

    assert df["rule_id"].is_unique


def test_rule_identifiers_are_not_null():
    df = generate_fraud_rules(count=8)

    assert df["rule_id"].notna().all()
    assert df["fraud_rule_key"].notna().all()


def test_rule_identifier_format():
    df = generate_fraud_rules(count=8)

    assert df["rule_id"].str.match(r"^RULE\d{3}$").all()


def test_rule_keys_are_sequential():
    df = generate_fraud_rules(count=8)

    assert df["fraud_rule_key"].tolist() == list(range(1, 9))


def test_rule_names_are_not_null():
    df = generate_fraud_rules(count=8)

    assert df["rule_name"].notna().all()
    assert (df["rule_name"].str.len() > 0).all()


def test_rule_descriptions_are_not_null():
    df = generate_fraud_rules(count=8)

    assert df["rule_description"].notna().all()
    assert (df["rule_description"].str.len() > 0).all()


def test_rule_categories_are_valid():
    df = generate_fraud_rules(count=8)

    assert set(df["rule_category"]).issubset(
        set(RULE_CATEGORIES)
    )


def test_rule_statuses_are_valid():
    df = generate_fraud_rules(count=8)

    assert set(df["rule_status"]).issubset(
        set(RULE_STATUSES)
    )


def test_alert_thresholds_are_valid():
    df = generate_fraud_rules(count=8)

    assert df["alert_threshold"].between(
        0.50,
        0.95,
    ).all()


def test_fraud_rule_generation_is_reproducible():
    df1 = generate_fraud_rules(
        count=8,
        seed=20260817,
    )

    df2 = generate_fraud_rules(
        count=8,
        seed=20260817,
    )

    pd.testing.assert_frame_equal(df1, df2)


def test_different_seed_changes_generated_attributes():
    df1 = generate_fraud_rules(
        count=8,
        seed=20260817,
    )

    df2 = generate_fraud_rules(
        count=8,
        seed=20260818,
    )

    assert not df1.equals(df2)


def test_invalid_count_is_rejected():
    with pytest.raises(ValueError):
        generate_fraud_rules(count=0)


def test_excessive_count_is_rejected():
    with pytest.raises(ValueError):
        generate_fraud_rules(count=9)
