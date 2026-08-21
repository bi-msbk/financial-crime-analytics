# Data Model

## Purpose

This document defines the conceptual and analytical data model for the Financial Crime Analytics & Fraud Detection Platform.

The model is derived from the approved data requirements, source-system design and business entities defined during Step 2.

The model is designed to support:

- SQL analysis
- Fraud analytics
- Behavioural analysis
- Control testing
- Machine learning
- Power BI reporting
- Reproducible analytical workflows

---

## 1. Modelling Approach

The project will use a relational analytical model that separates:

- Business dimensions
- Transaction events
- Fraud outcomes
- Fraud alerts
- Investigation events
- Fraud-monitoring controls

The model shall explicitly document the grain of each table.

This is necessary to prevent double-counting when transaction-level data is combined with alert-level and investigation-level data.

---

## 2. Analytical Model Structure

### Dimension / Master Entities

- dim_customer
- dim_account
- dim_merchant
- dim_device
- dim_geography
- dim_fraud_rule
- dim_date

### Fact / Event Entities

- fact_transaction
- fact_fraud_outcome
- fact_fraud_alert
- fact_investigation_case

---

## 3. Dimension Tables

### dim_customer

Represents the synthetic retail banking customer.

Primary key:

- customer_key

Business identifier:

- customer_id

Purpose:

- Customer segmentation
- Customer behavioural analysis
- Customer fraud analysis

---

### dim_account

Represents the synthetic banking account.

Primary key:

- account_key

Business identifier:

- account_id

Foreign key:

- customer_key

Purpose:

- Account activity
- Account exposure
- Customer-account analysis

---

### dim_merchant

Represents a synthetic merchant.

Primary key:

- merchant_key

Business identifier:

- merchant_id

Purpose:

- Merchant analysis
- Merchant-category analysis
- Merchant fraud analysis

---

### dim_device

Represents a synthetic device.

Primary key:

- device_key

Business identifier:

- device_id

Purpose:

- Device analysis
- Previously unseen device analysis
- Customer-device behaviour

---

### dim_geography

Represents geographic context.

Primary key:

- geography_key

Business identifier:

- geography_id

Purpose:

- Country analysis
- Region analysis
- Geographic anomaly analysis

---

### dim_fraud_rule

Represents a fraud-monitoring control.

Primary key:

- fraud_rule_key

Business identifier:

- rule_id

Purpose:

- Rule-level control analysis
- Detection analysis
- False-positive analysis

---

### dim_date

Represents calendar dates used for analytical reporting.

Primary key:

- date_key

Purpose:

- Daily analysis
- Weekly analysis
- Monthly analysis
- Quarterly analysis
- Yearly analysis
- Day-of-week analysis
- Seasonal analysis

---

## 4. Fact Tables

### fact_transaction

Represents the primary financial transaction event.

### Grain

> One row per transaction.

Primary key:

- transaction_key

Business identifier:

- transaction_id

Foreign keys include:

- customer_key
- account_key
- merchant_key
- device_key
- geography_key
- date_key

Transaction measures and attributes include:

- transaction_amount
- currency
- transaction_type
- transaction_channel
- transaction_status
- transaction_timestamp

This is the central analytical fact table.

---

### fact_fraud_outcome

Represents the subsequent determination of whether a transaction was confirmed as fraudulent.

### Grain

> One row per fraud outcome associated with a transaction.

Primary key:

- fraud_outcome_key

Business identifier:

- fraud_outcome_id

Foreign key:

- transaction_key

Attributes/measures include:

- fraud_flag
- fraud_type
- fraud_confirmed_date
- fraud_loss_amount
- fraud_outcome_source

A transaction may have zero or one fraud outcome in the analytical model.

---

### fact_fraud_alert

Represents a fraud-monitoring alert generated for a transaction.

### Grain

> One row per fraud alert generated for a transaction.

Primary key:

- alert_key

Business identifier:

- alert_id

Foreign keys:

- transaction_key
- fraud_rule_key
- date_key

Attributes include:

- alert_timestamp
- alert_status
- alert_outcome
- confirmed_fraud_flag

A transaction may generate multiple alerts.

---

### fact_investigation_case

Represents an investigation case associated with suspicious activity.

### Grain

> One row per investigation case.

Primary key:

- case_key

Business identifier:

- case_id

Foreign keys:

- alert_key
- transaction_key
- date_key

Attributes include:

- case_created_timestamp
- case_closed_timestamp
- case_priority
- case_status
- case_outcome

An alert may result in zero or one investigation case in the analytical model.

---

## 5. Conceptual Relationship Model

```text
                       dim_customer
                            â”‚
                            â”‚
                       dim_account
                            â”‚
                            â”‚
dim_merchant â”€â”€â”€â”€â”€â”€â”€ fact_transaction â”€â”€â”€â”€â”€â”€â”€ dim_device
                            â”‚
                            â”‚
                      dim_geography
                            â”‚
                            â”‚
                   fact_fraud_outcome
                            â”‚
                            â”‚
                     fact_fraud_alert
                            â”‚
                            â”œâ”€â”€â”€â”€ dim_fraud_rule
                            â”‚
                            â†“
                  fact_investigation_case

dim_date â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                         â”‚               â”‚               â”‚
                  fact_transaction  fact_fraud_alert  fact_investigation_case
