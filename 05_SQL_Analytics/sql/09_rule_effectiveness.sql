WITH rule_metrics AS (

    SELECT

        rule_id,

        COUNT(*) AS alert_count,

        SUM(
            CASE
                WHEN confirmed_fraud_flag = TRUE
                 AND alert_outcome = 'True Positive'
                THEN 1
                ELSE 0
            END
        ) AS true_positive_count,

        SUM(
            CASE
                WHEN confirmed_fraud_flag = FALSE
                 AND alert_outcome = 'False Positive'
                THEN 1
                ELSE 0
            END
        ) AS false_positive_count

    FROM read_parquet(
        '${DATA_DIR}/control_evaluation.parquet'
    )

    GROUP BY
        rule_id
)

SELECT

    rule_id,

    alert_count,

    true_positive_count,

    false_positive_count,

    ROUND(
        100.0
        * true_positive_count
        / NULLIF(
            true_positive_count + false_positive_count,
            0
        ),
        2
    ) AS precision_pct,

    ROUND(
        100.0
        * false_positive_count
        / NULLIF(
            alert_count,
            0
        ),
        2
    ) AS false_positive_share_pct,

    ROUND(
        100.0
        * alert_count
        / SUM(alert_count) OVER (),
        2
    ) AS alert_volume_share_pct

FROM rule_metrics

ORDER BY
    precision_pct DESC,
    alert_count DESC;
