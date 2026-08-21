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

ranked_customers AS (

    SELECT
        *,

        ROW_NUMBER() OVER (
            ORDER BY fraud_loss DESC, customer_key
        ) AS fraud_loss_rank,

        COUNT(*) OVER () AS active_customer_count

    FROM customer_activity
),

customer_bands AS (

    SELECT
        CASE
            WHEN fraud_loss_rank
                <= active_customer_count * 0.01
                THEN 'Top 1%'

            WHEN fraud_loss_rank
                <= active_customer_count * 0.05
                THEN 'Next 4%'

            WHEN fraud_loss_rank
                <= active_customer_count * 0.10
                THEN 'Next 5%'

            ELSE 'Remaining 90%'
        END AS customer_segment,

        fraud_transaction_count,

        fraud_loss

    FROM ranked_customers
)

SELECT
    customer_segment,

    COUNT(*) AS customer_count,

    SUM(fraud_transaction_count)
        AS fraud_transaction_count,

    ROUND(
        SUM(fraud_loss),
        2
    ) AS fraud_loss,

    ROUND(
        100.0
        * SUM(fraud_transaction_count)
        / SUM(SUM(fraud_transaction_count)) OVER (),
        2
    ) AS fraud_transaction_share_pct,

    ROUND(
        100.0
        * SUM(fraud_loss)
        / SUM(SUM(fraud_loss)) OVER (),
        2
    ) AS fraud_loss_share_pct

FROM customer_bands

GROUP BY
    customer_segment

ORDER BY
    CASE customer_segment
        WHEN 'Top 1%' THEN 1
        WHEN 'Next 4%' THEN 2
        WHEN 'Next 5%' THEN 3
        ELSE 4
    END;
