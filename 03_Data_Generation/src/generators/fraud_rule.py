from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "fraud_rule_key",
    "rule_id",
    "rule_name",
    "rule_category",
    "rule_description",
    "rule_status",
    "alert_threshold",
]


RULE_CATEGORIES = [
    "High Value",
    "High Velocity",
    "New Device",
    "Geographic Anomaly",
    "Unusual Timing",
    "Merchant Risk",
    "Behavioural Deviation",
    "Account Takeover",
]


RULE_STATUSES = [
    "Active",
    "Inactive",
]


RULE_DEFINITIONS = [
    (
        "High Value Transaction Rule",
        "High Value",
        "Identifies transactions with unusually high monetary values.",
    ),
    (
        "High Velocity Rule",
        "High Velocity",
        "Identifies unusually frequent transactions within a short period.",
    ),
    (
        "New Device Rule",
        "New Device",
        "Identifies transactions originating from previously unseen devices.",
    ),
    (
        "Geographic Anomaly Rule",
        "Geographic Anomaly",
        "Identifies transaction activity outside expected geographic patterns.",
    ),
    (
        "Unusual Timing Rule",
        "Unusual Timing",
        "Identifies transactions occurring at unusual times for the customer.",
    ),
    (
        "Merchant Risk Rule",
        "Merchant Risk",
        "Identifies activity associated with higher-risk merchant categories.",
    ),
    (
        "Behavioural Deviation Rule",
        "Behavioural Deviation",
        "Identifies transactions that materially differ from customer behaviour.",
    ),
    (
        "Account Takeover Rule",
        "Account Takeover",
        "Identifies combinations of indicators associated with account takeover-like activity.",
    ),
]


def generate_fraud_rules(
    count: int = 8,
    seed: int = 20260817,
) -> pd.DataFrame:
    """
    Generate a deterministic synthetic fraud-rule dimension.

    Grain:
        One row per fraud-monitoring rule.
    """

    if count <= 0:
        raise ValueError("count must be greater than zero")

    if count > len(RULE_DEFINITIONS):
        raise ValueError(
            f"count cannot exceed {len(RULE_DEFINITIONS)}"
        )

    rng = np.random.default_rng(seed)

    fraud_rule_key = np.arange(
        1,
        count + 1,
        dtype=np.int64,
    )

    rule_id = [
        f"RULE{i:03d}"
        for i in fraud_rule_key
    ]

    selected_definitions = RULE_DEFINITIONS[:count]

    rule_name = [
        definition[0]
        for definition in selected_definitions
    ]

    rule_category = [
        definition[1]
        for definition in selected_definitions
    ]

    rule_description = [
        definition[2]
        for definition in selected_definitions
    ]

    rule_status = rng.choice(
        RULE_STATUSES,
        size=count,
        p=[0.875, 0.125],
    )

    alert_threshold = rng.uniform(
        0.50,
        0.95,
        size=count,
    ).round(4)

    return pd.DataFrame(
        {
            "fraud_rule_key": fraud_rule_key,
            "rule_id": rule_id,
            "rule_name": rule_name,
            "rule_category": rule_category,
            "rule_description": rule_description,
            "rule_status": rule_status,
            "alert_threshold": alert_threshold,
        }
    )
