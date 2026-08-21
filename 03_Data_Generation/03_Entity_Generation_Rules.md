# Entity Generation Rules

## Purpose

This document defines the rules used to generate the business entities approved during Step 2.

Generation rules shall remain aligned with the Data Dictionary, Data Model, Relationships and Data Grain documentation.

---

## 1. Geography

Table:

`dim_geography`

Grain:

> One row per geographic reference entity.

The geography dataset shall contain:

- geography_id
- country
- region
- city or geographic_area
- latitude_band
- longitude_band

The geographic environment shall represent a fictional UK retail banking population.

---

## 2. Date

Table:

`dim_date`

Grain:

> One row per calendar date.

The date dimension shall support:

- Date.
- Year.
- Quarter.
- Month.
- Week.
- Day of week.
- Weekend indicator.
- Month-end indicator.

---

## 3. Customer

Table:

`dim_customer`

Grain:

> One row per customer.

Each customer shall have:

- customer_key
- customer_id
- customer_segment
- customer_age_band
- customer_region
- customer_status
- customer_onboarding_date

Customer identifiers shall be synthetic.

---

## 4. Account

Table:

`dim_account`

Grain:

> One row per account.

Each account shall have:

- account_key
- account_id
- customer_key
- customer_id
- account_type
- account_status
- account_open_date
- account_region

Every account shall reference a valid customer.

---

## 5. Merchant

Table:

`dim_merchant`

Grain:

> One row per merchant.

Each merchant shall have:

- merchant_key
- merchant_id
- merchant_name
- merchant_category
- merchant_region
- merchant_country
- merchant_status

Merchant names shall be synthetic.

---

## 6. Device

Table:

`dim_device`

Grain:

> One row per device.

Each device shall have:

- device_key
- device_id
- device_type
- operating_system
- device_first_seen_date
- device_region

Devices may be associated with multiple transactions.

---

## 7. Fraud Rule

Table:

`dim_fraud_rule`

Grain:

> One row per fraud-monitoring rule.

Each rule shall have:

- fraud_rule_key
- rule_id
- rule_name
- rule_category
- rule_description
- rule_status
- alert_threshold

Rules shall have different detection characteristics.

---

## 8. Transaction

Table:

`fact_transaction`

Grain:

> One row per financial transaction.

Each transaction shall reference:

- Customer.
- Account.
- Merchant where applicable.
- Device where applicable.
- Geography.
- Date.

Transaction generation shall establish normal behaviour before fraud scenarios are introduced.

---

## 9. Fraud Outcome

Table:

`fact_fraud_outcome`

Grain:

> One row per confirmed fraud outcome.

A transaction may have zero or one fraud outcome.

Fraud outcomes shall include:

- fraud_outcome_key
- fraud_outcome_id
- transaction_key
- transaction_id
- fraud_type
- fraud_confirmed_date
- fraud_loss_amount
- fraud_outcome_source

---

## 10. Fraud Alert

Table:

`fact_fraud_alert`

Grain:

> One row per fraud-monitoring alert.

A transaction may generate zero, one or multiple alerts.

Each alert shall reference:

- Transaction.
- Fraud rule.

---

## 11. Investigation Case

Table:

`fact_investigation_case`

Grain:

> One row per investigation case.

Each case shall reference:

- Alert where applicable.
- Transaction.

Cases shall support:

- Case priority.
- Case status.
- Case outcome.
- Creation timestamp.
- Closure timestamp.

---

## 12. Entity Generation Principle

Entities shall be generated in dependency order.

No child entity shall be generated without valid parent identifiers.

The generation process shall validate referential integrity before datasets are released.
