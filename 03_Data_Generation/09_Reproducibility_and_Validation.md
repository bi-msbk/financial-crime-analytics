
---

# 3.9 `09_Reproducibility_and_Validation.md`

```markdown
# Reproducibility and Validation

## Purpose

This document defines the controls required to reproduce and validate the synthetic data generation process.

The objective is to ensure that generated analytical datasets are traceable, internally consistent and reproducible.

---

## 1. Reproducibility Requirements

Each generation run shall record:

- Dataset version.
- Generation version.
- Configuration version.
- Random seed.
- Python version.
- Package versions.
- Generation timestamp.
- Reference period.
- Generation status.

---

## 2. Random Seed

A fixed random seed shall be used for controlled generation.

The seed shall be stored in:

`config/generation_config.yaml`

Changing the seed creates a new synthetic dataset variation and shall be documented.

---

## 3. Structural Validation

Validate that:

- All required datasets exist.
- All required columns exist.
- Required data types are correct.
- Expected table names are used.
- Output files are readable.

---

## 4. Completeness Validation

Validate critical fields including:

- Primary identifiers.
- Foreign keys.
- Transaction timestamps.
- Transaction amounts.
- Fraud indicators.
- Alert identifiers.
- Case identifiers.

Critical-field completeness shall meet the thresholds defined in Step 2.

---

## 5. Uniqueness Validation

Validate uniqueness of:

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

## 6. Referential Integrity Validation

Validate:

```text
Account â†’ Customer
Transaction â†’ Customer
Transaction â†’ Account
Transaction â†’ Merchant
Transaction â†’ Device
Transaction â†’ Geography
Fraud Outcome â†’ Transaction
Alert â†’ Transaction
Alert â†’ Fraud Rule
Investigation â†’ Alert
Investigation â†’ Transaction
