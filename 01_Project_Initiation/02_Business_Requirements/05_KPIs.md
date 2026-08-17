# KPI Catalogue

| ID      | KPI                         | Definition                                        | Calculation                            | Audience   |
|---------|---------------------------------------------------------------------------------|----------------------------------------|------------|
| KPI-001 | Total Transactions          | Number of transactions analysed                   | COUNT(transaction_id)                  | Executive  |
| KPI-002 | Fraud Transactions          | Confirmed fraudulent transactions                 | COUNT(fraud_transaction)               | Executive  |
| KPI-003 | Fraud Rate                  | Percentage of transactions confirmed fraudulent   | Fraud Transactions / Total Transactions| Executive  |
| KPI-004 | Gross Fraud Loss            | Total confirmed fraud loss                        | SUM(fraud_loss)                        | Executive  |
| KPI-005 | Average Fraud Value         | Average value of confirmed fraud                  | Fraud Loss / Fraud Transactions        | Executive  |
| KPI-006 | Control Detection Rate      | Fraud detected by existing controls               | Detected Fraud / Total Fraud           | Risk       |
| KPI-007 | Missed Fraud Rate           | Confirmed fraud not detected by controls          | Missed Fraud / Total Fraud             | Risk       |
| KPI-008 | False Positive Rate         | Non-fraud alerts relative to total alerts         | Non-Fraud Alerts / Total Alerts        | Operations |
| KPI-009 | Alert Conversion Rate       | Alerts resulting in confirmed fraud               | Confirmed Fraud Alerts / Total Alerts  | Operations |
| KPI-010 | High-Risk Cases             | Cases meeting high-risk criteria                  | COUNT(high_risk_case)                  | Operations |
| KPI-011 | Open Cases                  | Currently unresolved investigation cases          | COUNT(open_case)                       | Operations |
| KPI-012 | Average Investigation Time  | Average time to resolve a case                    | AVG(resolution_time)                   | Operations |








