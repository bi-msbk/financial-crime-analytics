SELECT
    COUNT(*) AS transaction_count,

    ROUND(
        SUM(transaction_amount),
        2
    ) AS total_transaction_value,

    SUM(
        CASE
            WHEN fraud_flag
            THEN 1
            ELSE 0
        END
    ) AS fraud_transaction_count,

    ROUND(
        100.0
        * SUM(
            CASE
                WHEN fraud_flag
                THEN 1
                ELSE 0
            END
        )
        / COUNT(*),
        4
    ) AS fraud_rate_pct,

    ROUND(
        SUM(fraud_loss_amount),
        2
    ) AS total_fraud_loss,

    ROUND(
        AVG(
            CASE
                WHEN fraud_flag
                THEN fraud_loss_amount
            END
        ),
        2
    ) AS average_fraud_loss,

    ROUND(
        AVG(transaction_amount),
        2
    ) AS average_transaction_amount,

    ROUND(
        MAX(transaction_amount),
        2
    ) AS maximum_transaction_amount

FROM read_parquet(
    '${DATA_DIR}/transaction.parquet'
);
