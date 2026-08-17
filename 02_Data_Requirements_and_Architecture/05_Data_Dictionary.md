# Data Dictionary

## Purpose

This document defines the field-level data dictionary for the Financial Crime Analytics & Fraud Detection Platform.

The dictionary provides the authoritative definition of fields used across:

- Synthetic data generation
- SQL analytics
- Python analytics
- Fraud detection
- Machine learning
- Power BI reporting
- Data-quality validation

Field definitions shall remain consistent throughout the project.

---

## 1. Key Conventions

### Surrogate Keys

Analytical tables use surrogate keys for dimensional relationships.

Examples:

- customer_key
- account_key
- merchant_key
- device_key
- geography_key
- fraud_rule_key
- date_key
- transaction_key
- fraud_outcome_key
- alert_key
- case_key

### Business Identifiers

Synthetic business identifiers are retained for traceability.

Examples:

- customer_id
- account_id
- merchant_id
- device_id
- geography_id
- rule_id
- transaction_id
- fraud_outcome_id
- alert_id
- case_id

---

# 2. Customer — dim_customer

| Field | Data Type | Key | Required | Definition | Example |
|---|---|---|---|---|---|
| customer_key | INTEGER | PK | Yes | Analytical surrogate key | 100001 |
| customer_id | STRING | Business ID | Yes | Unique synthetic customer identifier | CUST000001 |
| customer_segment | STRING | | Yes | Customer segmentation category | Mass Retail |
| customer_age_band | STRING | | Yes | Customer age grouping | 35-44 |
| customer_region | STRING | | Yes | Customer geographic region | London |
| customer_status | STRING | | Yes | Customer lifecycle status | Active |
| customer_onboarding_date | DATE | | Yes | Customer onboarding date | 2023-04-15 |

---

# 3. Account — dim_account

| Field | Data Type | Key | Required | Definition | Example |
|---|---|---|---|---|---|
| account_key | INTEGER | PK | Yes | Analytical surrogate key | 200001 |
| account_id | STRING | Business ID | Yes | Unique synthetic account identifier | ACC000001 |
| customer_key | INTEGER | FK | Yes | Customer owning the account | 100001 |
| account_type | STRING | | Yes | Account category | Current |
| account_status | STRING | | Yes | Account status | Active |
| account_open_date | DATE | | Yes | Account opening date | 2024-01-10 |
| account_region | STRING | | Yes | Account geographic region | London |

---

# 4. Merchant — dim_merchant

| Field | Data Type | Key | Required | Definition | Example |
|---|---|---|---|---|---|
| merchant_key | INTEGER | PK | Yes | Analytical surrogate key | 300001 |
| merchant_id | STRING | Business ID | Yes | Unique synthetic merchant identifier | MER000001 |
| merchant_name | STRING | | Yes | Synthetic merchant name | Northstar Retail |
| merchant_category | STRING | | Yes | Merchant category | Electronics |
| merchant_region | STRING | | Yes | Merchant region | London |
| merchant_country | STRING | | Yes | Merchant country | United Kingdom |
| merchant_status | STRING | | Yes | Merchant operating status | Active |

---

# 5. Device — dim_device

| Field | Data Type | Key | Required | Definition | Example |
|---|---|---|---|---|---|
| device_key | INTEGER | PK | Yes | Analytical surrogate key | 400001 |
| device_id | STRING | Business ID | Yes | Unique synthetic device identifier | DEV000001 |
| device_type | STRING | | Yes | Device category | Mobile |
| operating_system | STRING | | Yes | Device operating system | iOS |
| device_first_seen_date | DATE | | Yes | First date device was observed | 2024-06-01 |
| device_region | STRING | | Yes | Device geographic region | London |

---

# 6. Geography — dim_geography

| Field | Data Type | Key | Required | Definition | Example |
|---|---|---|---|---|---|
| geography_key | INTEGER | PK | Yes | Analytical surrogate key | 500001 |
| geography_id | STRING | Business ID | Yes | Unique synthetic geography identifier | GEO000001 |
| country | STRING | | Yes | Country | United Kingdom |
| region | STRING | | Yes | Geographic region | London |
| geographic_area | STRING | | Yes | City or geographic area | London Central |
| latitude_band | STRING | | Yes | Approximate latitude band | 51.x |
| longitude_band | STRING | | Yes | Approximate longitude band | 0.x |

Exact customer addresses will not be generated.

---

# 7. Fraud Rule — dim_fraud_rule

| Field | Data Type | Key | Required | Definition | Example |
|---|---|---|---|---|---|
| fraud_rule_key | INTEGER | PK | Yes | Analytical surrogate key | 600001 |
| rule_id | STRING | Business ID | Yes | Unique fraud rule identifier | RULE001 |
| rule_name | STRING | | Yes | Fraud rule name | High Velocity Rule |
| rule_category | STRING | | Yes | Rule classification | Velocity |
| rule_description | STRING | | Yes | Description of control logic | Multiple transactions within short period |
| rule_status | STRING | | Yes | Rule operating status | Active |
| alert_threshold | DECIMAL | | Conditional | Configured rule threshold where applicable | 5 |

---

# 8. Date — dim_date

| Field | Data Type | Key | Required | Definition | Example |
|---|---|---|---|---|---|
| date_key | INTEGER | PK | Yes | Analytical date key | 20260115 |
| calendar_date | DATE | | Yes | Calendar date | 2026-01-15 |
| year | INTEGER | | Yes | Calendar year | 2026 |
| quarter | STRING | | Yes | Calendar quarter | Q1 |
| month | INTEGER | | Yes | Calendar month number | 1 |
| month_name | STRING | | Yes | Calendar month name | January |
| week_number | INTEGER | | Yes | Calendar week | 3 |
| day_of_week | INTEGER | | Yes | Day number within week | 4 |
| day_name | STRING | | Yes | Day name | Thursday |
| is_weekend | BOOLEAN | | Yes | Weekend indicator | False |

---

# 9. Transaction — fact_transaction

### Grain

> One row per transaction.

| Field | Data Type | Key | Required | Definition | Example |
|---|---|---|---|---|---|
| transaction_key | INTEGER | PK | Yes | Analytical surrogate key | 70000001 |
| transaction_id | STRING | Business ID | Yes | Unique transaction identifier | TXN00000001 |
| customer_key | INTEGER | FK | Yes | Customer associated with transaction | 100001 |
| account_key | INTEGER | FK | Yes | Account associated with transaction | 200001 |
| merchant_key | INTEGER | FK | Conditional | Merchant associated with transaction | 300001 |
| device_key | INTEGER | FK | Conditional | Device associated with transaction | 400001 |
| geography_key | INTEGER | FK | Yes | Geographic context | 500001 |
| date_key | INTEGER | FK | Yes | Transaction calendar date | 20260115 |
| transaction_timestamp | DATETIME | | Yes | Transaction event timestamp | 2026-01-15 14:32:11 |
| transaction_amount | DECIMAL | | Yes | Monetary transaction amount | 1250.50 |
| currency | STRING | | Yes | Transaction currency | GBP |
| transaction_type | STRING | | Yes | Transaction type | Card Purchase |
| transaction_channel | STRING | | Yes | Transaction channel | Online |
| transaction_status | STRING | | Yes | Transaction processing status | Completed |

---

# 10. Fraud Outcome — fact_fraud_outcome

### Grain

> One row per fraud outcome associated with a transaction.

| Field | Data Type | Key | Required | Definition | Example |
|---|---|---|---|---|---|
| fraud_outcome_key | INTEGER | PK | Yes | Analytical surrogate key | 800001 |
| fraud_outcome_id | STRING | Business ID | Yes | Unique fraud outcome identifier | FOUT000001 |
| transaction_key | INTEGER | FK | Yes | Transaction associated with outcome | 70000001 |
| fraud_flag | BOOLEAN | | Yes | Confirmed fraud indicator | True |
| fraud_type | STRING | | Conditional | Fraud classification | Account Takeover |
| fraud_confirmed_date | DATE | | Conditional | Date fraud was confirmed | 2026-01-18 |
| fraud_loss_amount | DECIMAL | | Conditional | Confirmed financial loss | 1250.50 |
| fraud_outcome_source | STRING | | Yes | Source of fraud determination | Investigation |

---

# 11. Fraud Alert — fact_fraud_alert

### Grain

> One row per fraud alert generated for a transaction.

| Field | Data Type | Key | Required | Definition | Example |
|---|---|---|---|---|---|
| alert_key | INTEGER | PK | Yes | Analytical surrogate key | 900001 |
| alert_id | STRING | Business ID | Yes | Unique alert identifier | ALERT000001 |
| transaction_key | INTEGER | FK | Yes | Transaction generating alert | 70000001 |
| fraud_rule_key | INTEGER | FK | Yes | Rule generating alert | 600001 |
| date_key | INTEGER | FK | Yes | Alert calendar date | 20260115 |
| alert_timestamp | DATETIME | | Yes | Time alert was generated | 2026-01-15 14:35:10 |
| alert_status | STRING | | Yes | Current alert status | Closed |
| alert_outcome | STRING | | Yes | Alert investigation outcome | False Positive |
| confirmed_fraud_flag | BOOLEAN | | Yes | Whether alert resulted in confirmed fraud | False |

---

# 12. Investigation Case — fact_investigation_case

### Grain

> One row per investigation case.

| Field | Data Type | Key | Required | Definition | Example |
|---|---|---|---|---|---|
| case_key | INTEGER | PK | Yes | Analytical surrogate key | 1000001 |
| case_id | STRING | Business ID | Yes | Unique investigation identifier | CASE000001 |
| alert_key | INTEGER | FK | Conditional | Alert associated with case | 900001 |
| transaction_key | INTEGER | FK | Yes | Transaction associated with case | 70000001 |
| date_key | INTEGER | FK | Yes | Case creation calendar date | 20260115 |
| case_created_timestamp | DATETIME | | Yes | Case creation timestamp | 2026-01-15 15:00:00 |
| case_closed_timestamp | DATETIME | | Conditional | Case closure timestamp | 2026-01-17 10:30:00 |
| case_priority | STRING | | Yes | Investigation priority | High |
| case_status | STRING | | Yes | Investigation status | Closed |
| case_outcome | STRING | | Conditional | Investigation outcome | Confirmed Fraud |

---

# 13. Data Type Standards

The following logical data types shall be used consistently:

| Data Type | Purpose |
|---|---|
| INTEGER | Numeric identifiers and counts |
| STRING | Categorical and business identifier fields |
| DATE | Calendar dates |
| DATETIME | Event timestamps |
| DECIMAL | Monetary and numeric measures |
| BOOLEAN | True/False indicators |

The physical implementation may adapt these logical types to the selected database technology.

---

# 14. Key Standards

Primary keys shall uniquely identify records within their respective analytical tables.

Foreign keys shall reference valid parent records.

Business identifiers shall remain unique within their relevant business domain.

Surrogate keys shall be used for analytical relationships.

---

# 15. Nullability Principles

A field marked **Required = Yes** shall not contain null values in the validated analytical dataset unless an explicitly documented exception exists.

Conditional fields may be null when the corresponding business event has not occurred.

Examples:

- case_closed_timestamp may be null for open cases.
- fraud_confirmed_date may be null for non-fraudulent transactions.
- fraud_loss_amount may be null where no confirmed fraud loss exists.
- merchant_key may be null for transaction types that do not involve merchants.

---

# 16. Data Quality Expectations

The data dictionary shall provide the basis for data-quality validation.

Expected checks include:

- Primary-key uniqueness
- Foreign-key integrity
- Required-field completeness
- Valid categorical values
- Valid dates
- Valid timestamps
- Non-negative transaction amounts
- Non-negative fraud losses
- Valid fraud indicators
- Valid relationship cardinality
- Valid chronological relationships

---

# 17. Data Dictionary Governance

Changes to field definitions shall be version controlled.

Any new field, removed field or changed definition shall be documented before implementation.

The data dictionary shall remain aligned with:

Data Requirements → Data Model → Synthetic Data → Data Quality → SQL → Python → Machine Learning → Power BI.

