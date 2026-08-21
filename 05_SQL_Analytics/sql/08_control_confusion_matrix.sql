WITH transaction_alert_status AS (

    SELECT
        t.transaction_id,
        t.fraud_flag,

        CASE
            WHEN a.transaction_id IS NULL
                THEN FALSE
            ELSE TRUE
        END AS has_alert

    FROM read_parquet(
        '${DATA_DIR}/transaction.parquet'
    ) AS t

    LEFT JOIN (
        SELECT DISTINCT
            transaction_id
        FROM read_parquet(
            '${DATA_DIR}/control_evaluation.parquet'
        )
    ) AS a

        ON t.transaction_id = a.transaction_id
),

confusion_matrix AS (

    SELECT

        SUM(
            CASE
                WHEN fraud_flag = TRUE
                 AND has_alert = TRUE
                THEN 1
                ELSE 0
            END
        ) AS true_positive,

        SUM(
            CASE
                WHEN fraud_flag = FALSE
                 AND has_alert = TRUE
                THEN 1
                ELSE 0
            END
        ) AS false_positive,

        SUM(
            CASE
                WHEN fraud_flag = FALSE
                 AND has_alert = FALSE
                THEN 1
                ELSE 0
            END
        ) AS true_negative,

        SUM(
            CASE
                WHEN fraud_flag = TRUE
                 AND has_alert = FALSE
                THEN 1
                ELSE 0
            END
        ) AS false_negative

    FROM transaction_alert_status
)

SELECT

    true_positive,

    false_positive,

    true_negative,

    false_negative,

    ROUND(
        100.0 * true_positive
        / NULLIF(
            true_positive + false_negative,
            0
        ),
        2
    ) AS detection_rate_pct,

    ROUND(
        100.0 * false_positive
        / NULLIF(
            false_positive + true_negative,
            0
        ),
        4
    ) AS false_positive_rate_pct,

    ROUND(
        100.0 * true_positive
        / NULLIF(
            true_positive + false_positive,
            0
        ),
        2
    ) AS precision_pct,

    ROUND(
        100.0 * true_negative
        / NULLIF(
            true_negative + false_positive,
            0
        ),
        2
    ) AS specificity_pct,

    ROUND(
        2.0 * true_positive
        / NULLIF(
            2.0 * true_positive
            + false_positive
            + false_negative,
            0
        ),
        4
    ) AS f1_score

FROM confusion_matrix;
