# Data Quality Requirements

## Purpose

This document defines the data-quality requirements that shall be applied to the synthetic datasets and analytical tables used by the Financial Crime Analytics & Fraud Detection Platform.

The objective is to ensure that analytical results are:

- Complete
- Valid
- Consistent
- Referentially reliable
- Reproducible
- Internally plausible within the synthetic-data context

Because the project uses synthetic data, accuracy refers to internal logical consistency and realistic analytical behaviour rather than accuracy against real banking records.

---

## 1. Data Quality Dimensions

The project shall evaluate the following data-quality dimensions:

- Completeness
- Uniqueness
- Validity
- Consistency
- Referential integrity
- Temporal integrity
- Internal plausibility
- Accuracy within the synthetic-data context
- Timeliness where applicable

---

# 2. Data Quality Severity

| Severity | Definition |
|---|---|
| Critical | Failure may invalidate analytical results or break referential integrity |
| High | Failure may materially affect an analytical metric or business interpretation |
| Medium | Failure may affect a subset of analysis but does not invalidate the overall dataset |
| Low | Minor issue with limited analytical impact |

Critical failures shall be resolved or explicitly documented before the affected dataset is used for final analytical outputs.

---

# 3. Customer Data Rules

| ID | Rule | Severity |
|---|---|---|
| DQ-001 | `customer_id` must not be null | Critical |
| DQ-002 | `customer_id` must be unique | Critical |
| DQ-003 | `customer_status` must use an approved value | High |
| DQ-004 | `customer_segment` must use an approved value | Medium |
| DQ-005 | `customer_age_band` must use an approved value | Medium |
| DQ-006 | `customer_onboarding_date` must not be null | High |

---

# 4. Account Data Rules

| ID | Rule | Severity |
|---|---|---|
| DQ-007 | `account_id` must not be null | Critical |
| DQ-008 | `account_id` must be unique | Critical |
| DQ-009 | `customer_id` must exist in `dim_customer` | Critical |
| DQ-010 | `account_status` must use an approved value | High |
| DQ-011 | `account_type` must use an approved value | Medium |
| DQ-012 | `account_open_date` must not be null | High |
| DQ-013 | `account_open_date` must not precede customer onboarding date | High |

---

# 5. Merchant Data Rules

| ID | Rule | Severity |
|---|---|---|
| DQ-014 | `merchant_id` must not be null | Critical |
| DQ-015 | `merchant_id` must be unique | Critical |
| DQ-016 | `merchant_category` must use an approved value | High |
| DQ-017 | `merchant_country` must use an approved value | Medium |
| DQ-018 | `merchant_status` must use an approved value | Medium |

Merchant names are synthetic and shall not contain real customer information.

---

# 6. Device Data Rules

| ID | Rule | Severity |
|---|---|---|
| DQ-019 | `device_id` must not be null | Critical |
| DQ-020 | `device_id` must be unique | Critical |
| DQ-021 | `device_type` must use an approved value | Medium |
| DQ-022 | `operating_system` must use an approved value | Medium |
| DQ-023 | `device_first_seen_date` must not be null | High |

---

# 7. Geography Data Rules

| ID | Rule | Severity |
|---|---|---|
| DQ-024 | `geography_id` must be unique | Critical |
| DQ-025 | Country must use an approved value | High |
| DQ-026 | Region must correspond to the defined geographic hierarchy | High |
| DQ-027 | Geographic reference fields must use valid formats | Medium |

Exact customer addresses shall not be generated.

---

# 8. Transaction Data Rules

| ID | Rule | Severity |
|---|---|---|
| DQ-028 | `transaction_id` must not be null | Critical |
| DQ-029 | `transaction_id` must be unique | Critical |
| DQ-030 | `customer_id` must exist in `dim_customer` | Critical |
| DQ-031 | `account_id` must exist in `dim_account` | Critical |
| DQ-032 | `transaction_timestamp` must not be null | Critical |
| DQ-033 | `transaction_amount` must be greater than zero | Critical |
| DQ-034 | `currency` must use an approved value | High |
| DQ-035 | `transaction_type` must use an approved value | High |
| DQ-036 | `transaction_channel` must use an approved value | High |
| DQ-037 | `transaction_status` must use an approved value | High |
| DQ-038 | `fraud_flag` must contain valid Boolean values | Critical |
| DQ-039 | `transaction_timestamp` must not precede account opening date | High |
| DQ-040 | Merchant reference must exist where merchant is required | High |
| DQ-041 | Device reference must exist where device is required | High |

---

# 9. Fraud Outcome Data Rules

| ID | Rule | Severity |
|---|---|---|
| DQ-042 | `fraud_outcome_id` must not be null | Critical |
| DQ-043 | `fraud_outcome_id` must be unique | Critical |
| DQ-044 | `transaction_id` must exist in `fact_transaction` | Critical |
| DQ-045 | A transaction must have no more than one fraud outcome | Critical |
| DQ-046 | Confirmed fraud must have `fraud_flag = true` | Critical |
| DQ-047 | Confirmed fraud must have a defined fraud type | High |
| DQ-048 | Fraud loss must not be negative | Critical |
| DQ-049 | Non-fraud transactions must not contain confirmed fraud loss | High |
| DQ-050 | Fraud confirmation date must not precede transaction timestamp | High |

---

# 10. Fraud Rule Data Rules

| ID | Rule | Severity |
|---|---|---|
| DQ-051 | `rule_id` must not be null | Critical |
| DQ-052 | `rule_id` must be unique | Critical |
| DQ-053 | `rule_name` must not be null | High |
| DQ-054 | `rule_category` must use an approved value | Medium |
| DQ-055 | `rule_status` must use an approved value | High |

---

# 11. Fraud Alert Data Rules

| ID | Rule | Severity |
|---|---|---|
| DQ-056 | `alert_id` must not be null | Critical |
| DQ-057 | `alert_id` must be unique | Critical |
| DQ-058 | `transaction_id` must exist in `fact_transaction` | Critical |
| DQ-059 | `rule_id` must exist in `dim_fraud_rule` | Critical |
| DQ-060 | `alert_timestamp` must not be null | Critical |
| DQ-061 | `alert_timestamp` must not precede transaction timestamp | High |
| DQ-062 | `alert_status` must use an approved value | High |
| DQ-063 | `alert_outcome` must use an approved value | High |
| DQ-064 | `confirmed_fraud_flag` must contain valid Boolean values | Critical |

---

# 12. Investigation Case Data Rules

| ID | Rule | Severity |
|---|---|---|
| DQ-065 | `case_id` must not be null | Critical |
| DQ-066 | `case_id` must be unique | Critical |
| DQ-067 | `transaction_id` must exist in `fact_transaction` | Critical |
| DQ-068 | `alert_id` must exist where a case is created from an alert | High |
| DQ-069 | `case_created_timestamp` must not be null | Critical |
| DQ-070 | `case_created_timestamp` must not precede alert timestamp where an alert exists | High |
| DQ-071 | Closed cases must have a closure timestamp | High |
| DQ-072 | `case_closed_timestamp` must not precede case creation timestamp | Critical |
| DQ-073 | `case_status` must use an approved value | High |
| DQ-074 | `case_priority` must use an approved value | Medium |

---

# 13. Referential Integrity

The following relationships must be validated:

```text
Customer
   ↓
Account
   ↓
Transaction

