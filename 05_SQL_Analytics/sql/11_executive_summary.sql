WITH transaction_metrics AS (

    SELECT
        COUNT(*) AS transaction_count,

        SUM(transaction_amount) AS total_transaction_value,

        SUM(
            CASE
                WHEN fraud_flag = TRUE
                THEN 1
                ELSE 0
            END
        ) AS fraud_transaction_count,

        SUM(fraud_loss_amount) AS total_fraud_loss,

        AVG(transaction_amount) AS average_transaction_amount,

        MAX(transaction_amount) AS maximum_transaction_amount,

        AVG(
            CASE
                WHEN fraud_flag = TRUE
                THEN fraud_loss_amount
            END
        ) AS average_fraud_loss

    FROM read_parquet(
        '${DATA_DIR}/transaction.parquet'
    )
),

control_metrics AS (

    SELECT
        true_positive,
        false_positive,
        true_negative,
        false_negative,
        detection_rate_pct,
        false_positive_rate_pct,
        precision_pct,
        specificity_pct,
        f1_score

    FROM read_csv_auto(
        './05_SQL_Analytics/reports/control_confusion_matrix.csv'
    )
),

investigation_metrics AS (

    SELECT
        total_cases,
        closed_cases,
        open_cases,
        closure_rate_pct,
        open_case_rate_pct,
        high_priority_cases,
        medium_priority_cases,
        low_priority_cases,
        average_investigation_hours

    FROM read_csv_auto(
        './05_SQL_Analytics/reports/investigation_effectiveness.csv'
    )
)

SELECT

    t.transaction_count,

    ROUND(
        t.total_transaction_value,
        2
    ) AS total_transaction_value,

    t.fraud_transaction_count,

    ROUND(
        100.0
        * t.fraud_transaction_count
        / NULLIF(t.transaction_count, 0),
        2
    ) AS fraud_rate_pct,

    ROUND(
        t.total_fraud_loss,
        2
    ) AS total_fraud_loss,

    ROUND(
        t.average_fraud_loss,
        2
    ) AS average_fraud_loss,

    ROUND(
        t.average_transaction_amount,
        2
    ) AS average_transaction_amount,

    ROUND(
        t.maximum_transaction_amount,
        2
    ) AS maximum_transaction_amount,

    c.true_positive,

    c.false_positive,

    c.true_negative,

    c.false_negative,

    c.detection_rate_pct,

    c.false_positive_rate_pct,

    c.precision_pct,

    c.specificity_pct,

    c.f1_score,

    i.total_cases,

    i.closed_cases,

    i.open_cases,

    i.closure_rate_pct,

    i.open_case_rate_pct,

    i.high_priority_cases,

    i.medium_priority_cases,

    i.low_priority_cases,

    ROUND(
        i.average_investigation_hours,
        2
    ) AS average_investigation_hours

FROM transaction_metrics AS t

CROSS JOIN control_metrics AS c

CROSS JOIN investigation_metrics AS i;
