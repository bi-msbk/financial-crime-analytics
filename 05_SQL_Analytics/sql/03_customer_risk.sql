WITH channel_analysis AS (

    SELECT
        'Channel' AS analysis_dimension,

        transaction_channel AS segment,

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
            AVG(transaction_amount),
            2
        ) AS average_transaction_amount,

        ROUND(
            SUM(fraud_loss_amount),
            2
        ) AS fraud_loss

    FROM read_parquet(
        '${DATA_DIR}/transaction.parquet'
    )

    GROUP BY
        transaction_channel
),

transaction_type_analysis AS (

    SELECT
        'Transaction Type' AS analysis_dimension,

        transaction_type AS segment,

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
            AVG(transaction_amount),
            2
        ) AS average_transaction_amount,

        ROUND(
            SUM(fraud_loss_amount),
            2
        ) AS fraud_loss

    FROM read_parquet(
        '${DATA_DIR}/transaction.parquet'
    )

    GROUP BY
        transaction_type
)

SELECT *
FROM channel_analysis

UNION ALL

SELECT *
FROM transaction_type_analysis

ORDER BY
    analysis_dimension,
    fraud_rate_pct DESC;
