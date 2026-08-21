SELECT
    fraud_scenario,

    COUNT(*) AS fraud_transaction_count,

    ROUND(
        SUM(transaction_amount),
        2
    ) AS transaction_value,

    ROUND(
        SUM(fraud_loss_amount),
        2
    ) AS fraud_loss,

    ROUND(
        AVG(fraud_loss_amount),
        2
    ) AS average_fraud_loss,

    ROUND(
        100.0
        * COUNT(*)
        / SUM(COUNT(*)) OVER (),
        2
    ) AS fraud_transaction_share_pct,

    ROUND(
        100.0
        * SUM(fraud_loss_amount)
        / SUM(SUM(fraud_loss_amount)) OVER (),
        2
    ) AS fraud_loss_share_pct

FROM read_parquet(
    '${DATA_DIR}/transaction.parquet'
)

WHERE fraud_flag = TRUE

GROUP BY
    fraud_scenario

ORDER BY
    fraud_loss DESC;
