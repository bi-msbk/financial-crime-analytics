# Source System Design

## Purpose

This document defines the conceptual source-system architecture used to support the Financial Crime Analytics & Fraud Detection Platform.

The architecture is fictional and is intended to represent a realistic retail banking analytical environment.

It does not represent the internal systems, processes or architecture of any specific bank.

---

## 1. Conceptual Architecture

The project assumes the following conceptual source domains:

Customer Management
        ↓
Account Management
        ↓
Transaction / Payments Platform
        ↓
Merchant / Device / Geographic Services
        ↓
Fraud Monitoring
        ↓
Fraud Outcome Management
        ↓
Investigation Management
        ↓
Analytical Data Platform
        ↓
Fraud Analytics & Reporting

The conceptual architecture represents the logical flow of information rather than physical production systems.

---

## 2. Source Domains

| Source Domain | Primary Data | Analytical Purpose |
|---|---|---|
| Customer Management | Customer information | Customer segmentation and behavioural analysis |
| Account Management | Account information | Account-level activity and exposure |
| Payments / Transactions | Transaction activity | Transaction and fraud analysis |
| Merchant Management | Merchant information | Merchant and merchant-category risk |
| Device Intelligence | Device information | Device and unseen-device analysis |
| Geographic Services | Geographic information | Geographic behaviour and anomaly analysis |
| Fraud Monitoring | Fraud rules and alerts | Control effectiveness analysis |
| Fraud Outcome Management | Confirmed fraud outcomes and losses | Fraud exposure and loss analysis |
| Investigation Management | Investigation cases | Investigation prioritisation and case analysis |

---

## 3. Customer Management

The Customer Management source domain provides customer-level information.

It provides:

- Customer identifier
- Customer segment
- Customer age band
- Customer status
- Customer region
- Customer onboarding information

The customer identifier shall be synthetic and shall not contain real customer-identifying information.

---

## 4. Account Management

The Account Management source domain provides account-level information.

It provides:

- Account identifier
- Customer relationship
- Account type
- Account status
- Account opening information
- Account region

The source design shall support the relationship:

Customer → Account

---

## 5. Transaction / Payments Platform

The Transaction / Payments Platform is the primary transactional source.

It provides:

- Transaction identifier
- Customer identifier
- Account identifier
- Transaction timestamp
- Transaction amount
- Currency
- Transaction type
- Transaction channel
- Merchant identifier
- Device identifier
- Transaction country
- Transaction region
- Transaction status

The primary transaction dataset shall have one record per transaction.

The transaction dataset is the central source for downstream fraud analytics.

---

## 6. Merchant Management

The Merchant Management source domain provides merchant-level information.

It provides:

- Merchant identifier
- Merchant name
- Merchant category
- Merchant region
- Merchant country
- Merchant status

Merchant information will be entirely synthetic.

The source design shall support the relationship:

Merchant → Transaction

---

## 7. Device Intelligence

The Device Intelligence source domain provides device-level information.

It provides:

- Device identifier
- Device type
- Operating system
- Device first-seen date
- Device region

The source design shall support identification of devices that are new or previously unseen for a customer.

The source design shall support the relationship:

Device → Transaction

---

## 8. Geographic Services

The Geographic Services source domain provides geographic attributes associated with transactions and customer activity.

It provides:

- Country
- Region
- City or geographic area
- Latitude band
- Longitude band

Exact customer addresses shall not be generated.

The source design shall support geographic segmentation and unusual geographic activity analysis.

---

## 9. Fraud Monitoring Platform

The Fraud Monitoring Platform represents the conceptual fraud-control environment.

It provides:

- Fraud rules
- Rule configuration
- Rule status
- Alert thresholds
- Fraud alerts
- Alert outcomes
- Control detection outcomes

The source design shall support evaluation of individual fraud rules and overall fraud-control effectiveness.

The conceptual relationship is:

Transaction → Fraud Rule Evaluation → Fraud Alert

---

## 10. Fraud Outcome Management

The Fraud Outcome Management domain represents the subsequent determination of whether transaction activity was confirmed as fraudulent.

It provides:

- Transaction identifier
- Fraud flag
- Fraud type
- Fraud confirmation date
- Fraud loss amount
- Fraud outcome source

Fraud outcome information shall remain logically distinct from the original transaction event.

The conceptual relationship is:

Transaction → Fraud Outcome

This separation allows the project to distinguish transaction activity from the later fraud determination.

---

## 11. Investigation Management

The Investigation Management source domain represents the investigation process following fraud alerts.

It provides:

- Investigation case identifier
- Alert identifier
- Transaction identifier
- Case creation timestamp
- Case closure timestamp
- Case priority
- Case status
- Case outcome

The conceptual relationship is:

Fraud Alert → Investigation Case

This supports investigation prioritisation, open-case analysis and investigation-time analysis.

---

## 12. Analytical Data Platform

The conceptual source datasets are consolidated into an analytical data environment.

The analytical environment supports:

- Source-data validation
- Data-quality checks
- Data standardisation
- Data transformation
- Analytical modelling
- SQL analysis
- Python analysis
- Fraud detection analysis
- Machine learning
- Power BI reporting
- Control testing
- Reproducible analytical workflows

The analytical environment shall preserve the relationships between the source domains.

---

## 13. Source-to-Analytical Flow

The conceptual data flow is:

```text
Conceptual Source Domains
          ↓
Raw / Source-like Data
          ↓
Data Validation & Quality Checks
          ↓
Standardised Analytical Data
          ↓
SQL / Python / Fraud Analytics
          ↓
Machine Learning
          ↓
Power BI / Management Reporting
          ↓
Findings & Recommendations