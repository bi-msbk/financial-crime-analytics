SELECT
    transaction_channel AS channel,

    transaction_type,

    COUNT(*) AS transaction_count,

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
    ) AS fraud_loss,

    ROUND(
        AVG(transaction_amount),
        2
    ) AS average_transaction_amount

FROM read_parquet(
    '${DATA_DIR}/transaction.parquet'
)

GROUP BY
    transaction_channel,
    transaction_type

ORDER BY
    fraud_rate_pct DESC;
