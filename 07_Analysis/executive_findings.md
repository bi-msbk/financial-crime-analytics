# Executive Findings

## 1. Executive Overview

This project analyses a synthetic production-scale financial crime dataset containing 2,000,000 transactions across a 2024â€“2025 reference period.

The objective is to identify fraud patterns, understand customer and transaction risk, evaluate fraud-monitoring controls, assess rule effectiveness, and examine investigation operations.

The analysis combines:

- Python-based data generation
- Automated data-quality validation
- SQL-based fraud analytics
- Control-effectiveness analysis
- Investigation analysis
- Executive-level visualisation

> **Important:** The dataset is synthetic and is intended to demonstrate a production-scale financial crime analytics workflow. It does not represent real customer, bank, or institutional data.

---

## 2. Fraud Exposure

The dataset contains:

| Metric | Result |
|---|---:|
| Total transactions | 2,000,000 |
| Total transaction value | Â£181.995M |
| Fraud transactions | 30,000 |
| Fraud rate | 1.50% |
| Total simulated fraud loss | Â£11.86M |
| Average fraud loss | Â£395.33 |
| Maximum transaction amount | Â£7,628 |

### Finding

Fraud represents 1.50% of transaction volume but generates approximately Â£11.86M in simulated losses.

The scale of the dataset provides sufficient volume to examine fraud behaviour across multiple scenarios, channels, transaction types, customers and monitoring controls.

---

## 3. Fraud Scenario Analysis

Fraud losses are distributed across eight simulated fraud scenarios.

| Fraud Scenario | Fraud Transactions | Fraud Loss | Loss Share |
|---|---:|---:|---:|
| Account Takeover | 5,948 | Â£2.36M | 19.89% |
| High Velocity | 4,542 | Â£1.80M | 15.14% |
| New Device | 4,557 | Â£1.79M | 15.06% |
| High Value | 4,544 | Â£1.77M | 14.94% |
| Online Fraud | 2,980 | Â£1.20M | 10.11% |
| Geographic Anomaly | 2,956 | Â£1.19M | 10.01% |
| Behavioural Deviation | 2,986 | Â£1.18M | 9.97% |
| Merchant Risk | 1,487 | Â£0.58M | 4.88% |

### Finding

Account takeover is the largest individual fraud scenario, accounting for approximately 19.89% of simulated fraud loss.

The three next-largest scenarios â€” high velocity, new device and high value â€” each contribute approximately 15% of total fraud loss.

This indicates that fraud exposure is diversified rather than being driven by a single scenario.

---

## 4. Customer and Transaction Risk

Fraudulent transactions have substantially higher transaction values than non-fraudulent transactions.

| Population | Transactions | Avg Transaction | Median Transaction | Max Transaction |
|---|---:|---:|---:|---:|
| Fraud | 30,000 | Â£584.33 | Â£478.52 | Â£7,628 |
| Non-Fraud | 1,970,000 | Â£83.48 | Â£54.09 | Â£2,120 |

### Finding

The average fraudulent transaction amount is approximately seven times the average non-fraudulent transaction amount.

This indicates that transaction value is an important risk-discrimination dimension within the synthetic dataset.

However, transaction value should not be used as a standalone fraud indicator because fraud also occurs across behavioural, device, geographic and channel dimensions.

---

## 5. Channel and Transaction-Type Risk

Fraud rates vary significantly by channel.

| Channel | Fraud Rate |
|---|---:|
| Mobile | 2.20% |
| Online | 2.17% |
| Card Present | 0.67% |
| ATM | 0.66% |
| Branch | 0.63% |

### Finding

Mobile and Online channels have materially higher fraud rates than Card Present, ATM and Branch transactions.

The highest-risk channel/transaction-type combinations include:

| Channel | Transaction Type | Fraud Rate |
|---|---|---:|
| Mobile | Transfer | 4.00% |
| Online | Transfer | 3.87% |
| Mobile | Direct Debit | 1.82% |
| Online | Cash Withdrawal | 1.81% |
| Mobile | Cash Withdrawal | 1.76% |

### Finding

The combination of digital channels and transfers represents the strongest observed transaction-level risk concentration.

This suggests that monitoring strategies should consider interactions between channel and transaction type rather than treating each dimension independently.

---

## 6. Customer Concentration

Customer-level analysis shows that fraud exposure is not evenly distributed across the customer population.

The highest-risk customer segments account for a disproportionate share of fraud losses relative to their population size.

The Top 1% customer segment represents approximately:

- 363 customers
- 1,274 fraud transactions
- Â£970K in simulated fraud losses
- 8.18% of total fraud loss

### Finding

A relatively small population of customers contributes a disproportionately large share of fraud losses.

This supports the use of customer-level risk profiling and targeted monitoring rather than relying exclusively on transaction-level controls.

---

## 7. Control Effectiveness

The control evaluation produced the following confusion-matrix results:

| Metric | Result |
|---|---:|
| True positives | 28,825 |
| False positives | 79,080 |
| True negatives | 1,890,920 |
| False negatives | 1,175 |
| Detection rate | 96.08% |
| False-positive rate | 4.01% |
| Precision | 26.71% |
| Specificity | 95.99% |
| F1 score | 0.418 |

### Finding

The control demonstrates strong fraud detection, identifying 96.08% of fraudulent transactions.

However, precision is only 26.71%.

This means that although the control captures most fraudulent activity, a substantial proportion of generated alerts are associated with non-fraudulent transactions.

The resulting false-positive volume of 79,080 represents a significant potential operational workload.

### Business implication

The key challenge is therefore not simply increasing detection.

The more important optimisation opportunity is improving the balance between:

- fraud detection
- alert precision
- investigation workload
- customer friction

---

## 8. Rule Effectiveness

Rule-level analysis shows significant variation in precision.

| Rule | Alerts | Precision |
|---|---:|---:|
| RULE007 | 19,868 | 100.00% |
| RULE001 | 11,155 | 90.21% |
| RULE002 | 21,562 | 78.87% |
| RULE003 | 81,187 | 20.67% |
| RULE005 | 10,678 | 10.21% |

### Finding

Rule performance is highly uneven.

RULE007 and RULE001 demonstrate strong precision, while RULE003 and RULE005 generate substantially more false-positive activity.

RULE003 is particularly significant because it represents the largest alert volume among the evaluated rules while achieving only 20.67% precision.

### Business implication

Rule optimisation should prioritise high-volume, low-precision rules.

Potential approaches include:

- threshold refinement
- customer segmentation
- transaction-context enrichment
- rule combination
- behavioural features
- risk-based alert prioritisation

---

## 9. Investigation Effectiveness

The investigation dataset contains:

| Metric | Result |
|---|---:|
| Total cases | 144,450 |
| Closed cases | 99,465 |
| Open cases | 44,985 |
| Closure rate | 68.86% |
| Open-case rate | 31.14% |
| High-priority cases | 51,560 |
| Medium-priority cases | 49,302 |
| Low-priority cases | 43,588 |
| Average investigation duration | 5.08 hours |

### Finding

Approximately 31.14% of investigation cases remain open in the generated dataset.

The volume of open cases indicates meaningful operational workload and reinforces the importance of alert quality and prioritisation.

Reducing false-positive alerts could therefore have a secondary benefit by allowing investigators to focus more time on higher-value investigations.

---

## 10. Key Analytical Conclusions

### Conclusion 1 â€” Fraud exposure is material

The synthetic dataset contains Â£11.86M of simulated fraud loss across 30,000 fraudulent transactions.

### Conclusion 2 â€” Digital channels require stronger risk differentiation

Mobile and Online transactions show substantially higher fraud rates than Branch, ATM and Card Present transactions.

### Conclusion 3 â€” Transfers are a major risk concentration

Mobile and Online transfers produce the highest observed channel/transaction-type fraud rates.

### Conclusion 4 â€” Detection performance is strong but alert precision is weaker

The control detects 96.08% of fraud but achieves only 26.71% precision.

This creates a significant false-positive workload.

### Conclusion 5 â€” Rule performance provides an immediate optimisation opportunity

Rule-level precision varies substantially, with RULE003 and RULE005 requiring particular attention due to their low precision.

### Conclusion 6 â€” Investigation capacity is an important operational consideration

A 31.14% open-case rate demonstrates that alert volume and prioritisation have direct implications for investigation workload.

---

## 11. Limitations

This analysis has several important limitations.

### Synthetic data

The dataset is synthetic and does not represent real customer behaviour or actual financial crime activity.

### Simulated fraud mechanisms

Fraud scenarios, fraud outcomes and control behaviour were generated according to predefined configuration parameters.

### No real-world model validation

The analysis demonstrates analytical methodology rather than validating a fraud model against real historical outcomes.

### No causal inference

Observed relationships should be interpreted as analytical patterns within the synthetic dataset, not as evidence of causal relationships in real financial systems.

### Control metrics

Control effectiveness metrics reflect the simulated control and outcome-generation logic used in the project.

---

## Final Assessment

The project demonstrates an end-to-end financial crime analytics workflow from production-scale synthetic data generation through data-quality validation, SQL analysis, control evaluation, investigation analysis and executive visualisation.

The strongest analytical theme is the trade-off between **fraud detection and operational efficiency**.

The simulated control achieves high fraud detection coverage, but relatively low precision creates substantial false-positive workload.

Therefore, the most valuable next-stage optimisation is not simply to detect more fraud, but to improve **risk segmentation, rule precision and alert prioritisation while preserving strong detection coverage**.
