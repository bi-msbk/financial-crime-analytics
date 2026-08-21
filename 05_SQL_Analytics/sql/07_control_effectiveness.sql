WITH alert_population AS (

    SELECT
        confirmed_fraud_flag,
        alert_outcome,

        COUNT(*) AS alert_count

    FROM read_parquet(
        '${DATA_DIR}/control_evaluation.parquet'
    )

    GROUP BY
        confirmed_fraud_flag,
        alert_outcome
),

metrics AS (

    SELECT

        SUM(alert_count) AS total_alerts,

        SUM(
            CASE
                WHEN confirmed_fraud_flag = TRUE
                 AND alert_outcome = 'True Positive'
                THEN alert_count
                ELSE 0
            END
        ) AS true_positive_alerts,

        SUM(
            CASE
                WHEN confirmed_fraud_flag = FALSE
                 AND alert_outcome = 'False Positive'
                THEN alert_count
                ELSE 0
            END
        ) AS false_positive_alerts,

        SUM(
            CASE
                WHEN confirmed_fraud_flag = TRUE
                 AND alert_outcome = 'False Negative'
                THEN alert_count
                ELSE 0
            END
        ) AS false_negative_alerts

    FROM alert_population
)

SELECT

    total_alerts,

    true_positive_alerts,

    false_positive_alerts,

    false_negative_alerts,

    ROUND(
        100.0
        * true_positive_alerts
        / NULLIF(
            true_positive_alerts
            + false_negative_alerts,
            0
        ),
        2
    ) AS detection_rate_pct,

    ROUND(
        100.0
        * false_positive_alerts
        / NULLIF(
            false_positive_alerts
            + true_positive_alerts,
            0
        ),
        2
    ) AS false_positive_rate_among_alerts_pct,

    ROUND(
        100.0
        * true_positive_alerts
        / NULLIF(
            true_positive_alerts
            + false_positive_alerts,
            0
        ),
        2
    ) AS precision_pct

FROM metrics;
