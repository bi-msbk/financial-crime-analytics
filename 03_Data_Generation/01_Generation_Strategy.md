# Generation Strategy

## Purpose

This document defines the strategy for generating the synthetic data required by the Financial Crime Analytics & Fraud Detection Platform.

The generation strategy is derived from the approved Step 2 â€” Data Requirements & Architecture documentation.

The objective is to create a realistic but fictional UK retail banking analytical environment that supports fraud analysis, behavioural analysis, fraud-control testing, investigation analysis, machine learning and management reporting.

No real customer information, personally identifiable information or confidential banking data will be used.

---

## 1. Generation Objectives

The synthetic data generation process shall:

- Create all approved analytical entities.
- Maintain the approved data model.
- Maintain the approved grain of each table.
- Maintain referential integrity.
- Generate realistic customer and transaction behaviour.
- Generate non-trivial fraud patterns.
- Simulate imperfect fraud-monitoring controls.
- Simulate fraud alerts and investigations.
- Support all approved KPIs and analytical questions.
- Support SQL, Python, machine-learning and Power BI analysis.
- Produce reproducible datasets.
- Produce validation results and generation metadata.

---

## 2. Approved Analytical Entities

The generation process shall produce:

| Entity | Analytical Table |
|---|---|
| Customer | `dim_customer` |
| Account | `dim_account` |
| Merchant | `dim_merchant` |
| Device | `dim_device` |
| Geography | `dim_geography` |
| Fraud Rule | `dim_fraud_rule` |
| Date | `dim_date` |
| Transaction | `fact_transaction` |
| Fraud Outcome | `fact_fraud_outcome` |
| Fraud Alert | `fact_fraud_alert` |
| Investigation Case | `fact_investigation_case` |

---

## 3. Generation Sequence

Generation shall follow dependency order:

```text
Configuration
      â†“
Geography
      â†“
Date
      â†“
Customers
      â†“
Accounts
      â†“
Merchants
      â†“
Devices
      â†“
Fraud Rules
      â†“
Normal Transaction Behaviour
      â†“
Fraud Scenario Assignment
      â†“
Fraud Outcomes
      â†“
Fraud Rule Evaluation
      â†“
Fraud Alerts
      â†“
Investigation Cases
      â†“
Validation
      â†“
Final Analytical Dataset
