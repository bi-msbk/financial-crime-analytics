WITH customer_activity AS (

    SELECT
        customer_key,

        COUNT(*) AS transaction_count,

        SUM(transaction_amount) AS transaction_value,

        SUM(
            CASE
                WHEN fraud_flag
                THEN 1
                ELSE 0
            END
        ) AS fraud_transaction_count,

        SUM(fraud_loss_amount) AS fraud_loss

    FROM read_parquet(
        '${DATA_DIR}/transaction.parquet'
    )

    GROUP BY
        customer_key
),

customer_risk AS (

    SELECT
        customer_key,

        transaction_count,

        ROUND(
            transaction_value,
            2
        ) AS transaction_value,

        fraud_transaction_count,

        ROUND(
            100.0
            * fraud_transaction_count
            / transaction_count,
            4
        ) AS fraud_rate_pct,

        ROUND(
            fraud_loss,
            2
        ) AS fraud_loss,

        ROUND(
            transaction_value
            / transaction_count,
            2
        ) AS average_transaction_amount

    FROM customer_activity
)

SELECT
    *
FROM customer_risk

ORDER BY
    fraud_loss DESC;
