WITH investigation_metrics AS (

    SELECT

        COUNT(*) AS total_cases,

        SUM(
            CASE
                WHEN case_status = 'Closed'
                THEN 1
                ELSE 0
            END
        ) AS closed_cases,

        SUM(
            CASE
                WHEN case_status = 'Open'
                THEN 1
                ELSE 0
            END
        ) AS open_cases,

        SUM(
            CASE
                WHEN case_priority = 'High'
                THEN 1
                ELSE 0
            END
        ) AS high_priority_cases,

        SUM(
            CASE
                WHEN case_priority = 'Medium'
                THEN 1
                ELSE 0
            END
        ) AS medium_priority_cases,

        SUM(
            CASE
                WHEN case_priority = 'Low'
                THEN 1
                ELSE 0
            END
        ) AS low_priority_cases,

        SUM(
            CASE
                WHEN case_outcome = 'Confirmed Fraud'
                THEN 1
                ELSE 0
            END
        ) AS confirmed_fraud_cases,

        SUM(
            CASE
                WHEN case_outcome = 'False Positive'
                THEN 1
                ELSE 0
            END
        ) AS false_positive_cases,

        AVG(
            CASE
                WHEN investigation_duration IS NOT NULL
                THEN investigation_duration
            END
        ) AS average_investigation_hours

    FROM read_parquet(
        '${DATA_DIR}/investigation.parquet'
    )
)

SELECT

    total_cases,

    closed_cases,

    open_cases,

    ROUND(
        100.0 * closed_cases
        / NULLIF(total_cases, 0),
        2
    ) AS closure_rate_pct,

    ROUND(
        100.0 * open_cases
        / NULLIF(total_cases, 0),
        2
    ) AS open_case_rate_pct,

    high_priority_cases,

    medium_priority_cases,

    low_priority_cases,

    confirmed_fraud_cases,

    false_positive_cases,

    ROUND(
        100.0 * confirmed_fraud_cases
        / NULLIF(
            confirmed_fraud_cases
            + false_positive_cases,
            0
        ),
        2
    ) AS confirmed_fraud_rate_pct,

    ROUND(
        average_investigation_hours,
        2
    ) AS average_investigation_hours

FROM investigation_metrics;
