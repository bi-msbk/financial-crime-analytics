# Synthetic Data Specification

## Purpose

This document defines the approved specification for generating synthetic data for the Financial Crime Analytics & Fraud Detection Platform.

The synthetic dataset shall represent a realistic but fictional UK retail banking environment and shall support the analytical requirements established during Project Initiation and Data Requirements & Architecture.

The specification provides the controlled handover from Step 2 â€” Data Requirements & Architecture to Step 3 â€” Data Generation.

No real customer information, personally identifiable information or confidential banking data shall be used.

---

# 1. Synthetic Data Principles

The generated data shall:

- Be completely synthetic.
- Contain no real customer PII.
- Represent a realistic but fictional UK retail banking environment.
- Support transaction-level fraud analysis.
- Support customer behavioural analysis.
- Support account-level analysis.
- Support merchant and channel analysis.
- Support device analysis.
- Support geographic analysis.
- Support transaction-velocity analysis.
- Support fraud-control effectiveness analysis.
- Support investigation analysis.
- Support SQL analytics.
- Support Python analytics.
- Support machine-learning analysis.
- Support Power BI reporting.
- Be reproducible using documented generation logic.
- Maintain referential integrity.
- Maintain the approved table grains.
- Contain non-trivial but analytically identifiable fraud patterns.

---

# 2. Data Scope

Synthetic data shall be generated for the following analytical entities:

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

# 3. Synthetic Environment

The dataset shall represent a fictional UK retail banking environment.

The conceptual environment shall contain:

- UK customers
- UK banking accounts
- UK and selected international transaction locations
- Retail merchants
- Online and physical transaction channels
- Multiple device types
- Fraud-monitoring controls
- Fraud alerts
- Investigation cases

The environment shall not represent the actual internal systems, controls, customers or processes of any named bank.

---

# 4. Reference Period

The initial synthetic analytical period shall cover:

> **1 January 2024 to 31 December 2025**

This provides two full years of transaction history for:

- Trend analysis
- Seasonality analysis
- Customer behavioural baselines
- Fraud trend analysis
- Time-based feature engineering
- Model development

The exact period may be adjusted during implementation if required, but any change shall be documented.

---

# 5. Target Data Volumes

The initial target volumes shall be:

| Entity | Target Volume |
|---|---:|
| Customers | 50,000 |
| Accounts | 65,000 |
| Merchants | 5,000 |
| Devices | 75,000 |
| Geography | 100â€“250 |
| Fraud Rules | 15â€“25 |
| Transactions | 2,000,000 |
| Fraud Outcomes | Approximately 20,000â€“40,000 |
| Fraud Alerts | Approximately 100,000â€“250,000 |
| Investigation Cases | Approximately 30,000â€“80,000 |

These are target ranges rather than mandatory exact counts.

Final generated volumes shall be recorded after generation.

---

# 6. Customer Generation

Customers shall be generated with:

- Unique `customer_id`
- Customer segment
- Age band
- Region
- Customer status
- Onboarding date

Customer segments shall contain realistic variation.

Example segments:

- Mass Retail
- Affluent
- Young Adult
- Senior
- Small Business / Sole Trader where applicable

Customer activity levels shall vary so that some customers have:

- Low transaction frequency
- Medium transaction frequency
- High transaction frequency

This variation will support behavioural-baseline analysis.

---

# 7. Account Generation

Each customer shall have one or more accounts according to the defined synthetic relationship rules.

The majority of customers should have one account, while a smaller proportion should have multiple accounts.

Account attributes shall include:

- Account type
- Account status
- Account opening date
- Customer relationship
- Account region

Account opening dates must not precede customer onboarding dates.

---

# 8. Merchant Generation

Merchants shall be synthetic.

Merchant attributes shall include:

- Merchant identifier
- Synthetic merchant name
- Merchant category
- Merchant region
- Merchant country
- Merchant status

Merchant categories shall contain sufficient variation to support merchant-risk analysis.

Example categories:

- Grocery
- Restaurants
- Travel
- Electronics
- Clothing
- Fuel
- Entertainment
- Online Retail
- Digital Services
- Financial Services

---

# 9. Device Generation

Devices shall be synthetic.

Device attributes shall include:

- Device identifier
- Device type
- Operating system
- First-seen date
- Geographic region

Customers shall normally use a limited number of recurring devices.

A smaller number of transactions shall involve previously unseen or newly associated devices.

This will support:

> New-device risk analysis.

---

# 10. Geography Generation

Geographic data shall support:

- Customer region
- Account region
- Transaction country
- Transaction region
- Geographic area

The majority of transactions should occur within expected customer geographies.

A smaller proportion of transactions should occur outside normal customer geographic patterns.

This will support:

> Unusual geographic activity analysis.

Exact residential addresses shall not be generated.

---

# 11. Transaction Generation

`fact_transaction` shall use the following grain:

> One row per financial transaction.

Each transaction shall include:

- Transaction identifier
- Customer
- Account
- Timestamp
- Amount
- Currency
- Transaction type
- Channel
- Merchant
- Device
- Geography
- Transaction status
- Fraud indicator

Transaction amounts shall follow a non-uniform distribution.

The dataset shall contain:

- Small everyday transactions
- Medium-value transactions
- Higher-value transactions
- Occasional extreme values

This supports transaction-amount anomaly analysis.

---

# 12. Transaction Channels

The synthetic dataset shall contain multiple transaction channels.

Example distribution:

| Channel | Target Share |
|---|---:|
| Card Present | 40% |
| Online | 30% |
| Mobile | 15% |
| Bank Transfer | 10% |
| ATM | 5% |

The final distribution shall be validated after generation.

---

# 13. Transaction Types

Example transaction types shall include:

- Card Purchase
- Online Purchase
- Cash Withdrawal
- Bank Transfer
- Direct Debit
- Mobile Payment

The exact transaction types shall remain consistent with the Data Dictionary.

---

# 14. Temporal Behaviour

Transactions shall vary across:

- Hour of day
- Day of week
- Month
- Season
- Weekday/weekend

The dataset shall support analysis of:

- Peak transaction periods
- Unusual transaction times
- Weekend behaviour
- Seasonal behaviour

Fraud shall not be uniformly distributed across time.

---

# 15. Customer Behaviour Baselines

Customer transaction behaviour shall be generated with persistent individual patterns.

For example, customers may have different:

- Typical transaction amounts
- Typical transaction frequency
- Typical transaction channels
- Typical merchant categories
- Typical geographic locations
- Typical devices

Fraudulent activity should sometimes represent a deviation from the customer's historical baseline.

This supports behavioural-anomaly analysis.

---

# 16. Transaction Velocity

The dataset shall contain transaction sequences that allow calculation of velocity indicators.

Examples:

- Number of transactions within 5 minutes
- Number of transactions within 30 minutes
- Number of transactions within 1 hour
- Number of transactions within 24 hours

A subset of fraudulent activity shall exhibit elevated transaction velocity.

Velocity shall not be perfectly deterministic of fraud.

---

# 17. Fraud Prevalence

Fraud shall represent a minority of transactions.

Initial target:

> Approximately **1%â€“2% of transactions** shall be confirmed fraudulent.

The final prevalence shall be measured after data generation.

Fraud prevalence shall not be so high that the dataset ceases to represent a realistic fraud-detection problem.

---

# 18. Fraud Types

Synthetic fraud outcomes shall contain multiple fraud categories.

Example categories:

- Account Takeover
- Card Payment Fraud
- Online Purchase Fraud
- Payment Fraud
- Cash Withdrawal Fraud
- Other Suspicious Transaction

Fraud types shall have different behavioural characteristics.

No single indicator shall perfectly identify a fraud type.

---

# 19. Fraud Pattern Design

Fraudulent activity shall contain combinations of risk indicators.

Potential indicators include:

- High transaction amount
- High transaction velocity
- New device
- Unusual geography
- Unusual transaction time
- Unusual merchant category
- Behavioural deviation
- Rapid sequence of transactions
- Unusual channel usage

Fraud patterns shall overlap.

For example:

```text
New Device
    +
Unusual Geography
    +
High Velocity
    â†“
Higher Fraud Risk
