
---

# 3.2 `02_Generation_Configuration.md`

```markdown
# Generation Configuration

## Purpose

This document defines the configurable parameters used by the synthetic data generation process.

Configuration values shall be maintained separately from generation logic wherever practical.

The authoritative machine-readable configuration will be maintained in:

`config/generation_config.yaml`

---

## 1. Environment Configuration

| Parameter | Initial Value |
|---|---|
| Project | Financial Crime Analytics & Fraud Detection Platform |
| Dataset Version | v1.0 |
| Generation Version | v1.0 |
| Random Seed | 20260817 |
| Reference Start Date | 2024-01-01 |
| Reference End Date | 2025-12-31 |
| Base Currency | GBP |
| Geographic Context | UK retail banking |

These values are configurable and may be revised during validation.

---

## 2. Initial Data Volume Targets

The following values are initial generation targets rather than fixed business requirements.

| Entity | Initial Target |
|---|---:|
| Customers | 50,000 |
| Accounts | 65,000 |
| Merchants | 5,000 |
| Devices | 75,000 |
| Transactions | 2,000,000 |
| Fraud Outcomes | Configurable |
| Fraud Alerts | Configurable |
| Investigation Cases | Configurable |

Final achieved volumes shall be recorded in the Step 3 generation summary.

---

## 3. Customer Configuration

Customer generation shall support:

- Customer segments.
- Age bands.
- Geographic regions.
- Customer status.
- Onboarding dates.
- Multiple accounts per customer.

The customer distribution shall avoid unrealistic concentration in a single segment or region.

---

## 4. Account Configuration

Account generation shall support:

- Multiple accounts per customer.
- Account types.
- Account status.
- Account opening dates.
- Customer-account referential integrity.

---

## 5. Transaction Configuration

Transaction generation shall support:

- Transaction types.
- Transaction channels.
- Transaction amounts.
- Transaction timestamps.
- Merchant relationships.
- Device relationships.
- Geographic attributes.
- Transaction status.
- Fraud outcomes.

---

## 6. Behaviour Configuration

Configurable behavioural parameters shall include:

- Average transaction frequency.
- Transaction amount distributions.
- Channel preferences.
- Merchant-category preferences.
- Device reuse.
- Geographic activity.
- Time-of-day patterns.
- Day-of-week patterns.
- Customer behavioural variation.

---

## 7. Fraud Configuration

Fraud configuration shall include:

- Target fraud prevalence.
- Fraud scenario weights.
- Fraud-risk multipliers.
- Fraud-loss assumptions.
- Behavioural deviation parameters.
- High-value transaction thresholds.
- Velocity thresholds.
- New-device parameters.
- Geographic anomaly parameters.

Fraud prevalence shall remain configurable and shall be validated against the final generated dataset.

---

## 8. Control Configuration

Fraud-monitoring configuration shall include:

- Rule definitions.
- Rule thresholds.
- Rule status.
- Detection effectiveness.
- False-positive behaviour.
- Alert-generation probability.
- Missed-fraud behaviour.

---

## 9. Investigation Configuration

Investigation configuration shall include:

- Case creation probability.
- Priority distribution.
- Case status distribution.
- Investigation duration.
- Case outcome distribution.
- Open-case proportion.

---

## 10. Configuration Governance

Configuration changes shall be version controlled.

Generation results shall record:

- Dataset version.
- Generation version.
- Configuration version.
- Random seed.
- Generation timestamp.

This ensures that a generated dataset can be traced back to the configuration used to create it.
