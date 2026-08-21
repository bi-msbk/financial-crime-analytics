# Data Grain

## Purpose

This document defines the grain of each analytical table used by the Financial Crime Analytics & Fraud Detection Platform.

Grain specifies exactly what one row represents in a table.

Clearly defined grain is required to:

- Prevent double-counting.
- Maintain analytical consistency.
- Support reliable SQL aggregation.
- Support accurate Power BI measures.
- Support reproducible analytical workflows.
- Support correct machine-learning feature construction.

---

## 1. Dimension Grain

### Customer

Table:

`dim_customer`

Grain:

> One row per customer.

Each customer is represented once in the analytical customer dimension.

---

### Account

Table:

`dim_account`

Grain:

> One row per account.

Each account is represented once in the analytical account dimension.

---

### Merchant

Table:

`dim_merchant`

Grain:

> One row per merchant.

Each merchant is represented once in the analytical merchant dimension.

---

### Device

Table:

`dim_device`

Grain:

> One row per device.

Each device is represented once in the analytical device dimension.

---

### Geography

Table:

`dim_geography`

Grain:

> One row per geographic reference entity.

Each geography record represents a defined geographic reference used for analytical segmentation.

---

### Fraud Rule

Table:

`dim_fraud_rule`

Grain:

> One row per fraud-monitoring rule.

Each rule represents one defined fraud-monitoring control.

---

### Date

Table:

`dim_date`

Grain:

> One row per calendar date.

Each date represents one calendar day used for analytical reporting.

---

# 2. Fact Grain

## 2.1 Transaction Grain

Table:

`fact_transaction`

Grain:

> One row per financial transaction.

This is the primary analytical event grain.

Each transaction record represents one financial transaction occurring at a specific point in time.

A transaction may be associated with:

- One customer
- One account
- Zero or one merchant
- Zero or one device
- One geography
- One transaction date

---

## 2.2 Fraud Outcome Grain

Table:

`fact_fraud_outcome`

Grain:

> One row per fraud outcome associated with a transaction.

A transaction may have zero or one fraud outcome in the analytical model.

A fraud outcome represents the subsequent determination of whether the transaction was confirmed as fraudulent and, where applicable, the associated financial loss.

---

## 2.3 Fraud Alert Grain

Table:

`fact_fraud_alert`

Grain:

> One row per fraud-monitoring alert generated.

A single transaction may generate multiple fraud alerts.

For example:

```text
Transaction TXN001
    â”œâ”€â”€ Alert A001 â€” Velocity Rule
    â”œâ”€â”€ Alert A002 â€” Unusual Amount Rule
    â””â”€â”€ Alert A003 â€” New Device Rule
