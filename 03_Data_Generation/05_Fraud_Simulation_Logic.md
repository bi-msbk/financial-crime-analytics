# Fraud Simulation Logic

## Purpose

This document defines the logic used to introduce synthetic fraud scenarios into the generated transaction population.

Fraud shall represent a minority of total transactions and shall contain identifiable but non-trivial behavioural patterns.

---

## 1. Fraud Simulation Principle

Fraud shall be generated using combinations of risk indicators rather than a single deterministic rule.

The objective is to create a dataset suitable for:

- Fraud pattern analysis.
- Anomaly detection.
- Risk scoring.
- Machine learning.
- Control effectiveness analysis.

---

## 2. Fraud Scenarios

The simulation shall support:

1. Account takeover.
2. High-value transaction fraud.
3. High-velocity fraud.
4. New-device fraud.
5. Geographic anomaly.
6. Online transaction fraud.
7. Merchant-category-related fraud.
8. Behavioural deviation.

---

## 3. Account Takeover

Account-takeover-like activity may contain combinations such as:

- Previously unseen device.
- Unusual geography.
- Unusual transaction time.
- Changed transaction behaviour.
- Increased transaction velocity.
- Higher-than-normal transaction amounts.

No single indicator shall guarantee fraud.

---

## 4. High-Value Fraud

High-value fraud shall contain transactions whose amounts are unusually high relative to:

- Customer baseline.
- Account activity.
- Normal transaction distribution.

Some legitimate high-value transactions shall also exist.

---

## 5. Velocity Fraud

Velocity-related fraud shall contain unusually high transaction activity within short time windows.

Some legitimate high-frequency activity shall also exist.

---

## 6. New-Device Fraud

A proportion of fraudulent activity shall occur from devices not previously associated with the customer.

New-device transactions shall also occur legitimately.

---

## 7. Geographic Fraud

Fraud scenarios may include activity outside a customer's normal geographic pattern.

Legitimate geographic variation shall also exist.

---

## 8. Behavioural Deviation

Fraudulent activity may differ from the customer's established baseline in:

- Amount.
- Frequency.
- Channel.
- Merchant category.
- Device.
- Geography.
- Time.

---

## 9. Fraud Classification

Each confirmed fraud outcome shall receive a synthetic fraud type.

Fraud types shall be documented and consistently used throughout the project.

---

## 10. Fraud Loss

Confirmed fraud shall have a non-negative fraud loss amount.

The loss amount shall be logically related to the fraudulent transaction value.

Non-fraud transactions shall not receive confirmed fraud loss.

---

## 11. Fraud Imbalance

Fraud shall remain a minority class.

Initial target prevalence is configurable through:

`config/generation_config.yaml`

The final prevalence shall be measured and reported after generation.

---

## 12. Non-Deterministic Fraud

Fraud indicators shall overlap with legitimate activity.

Therefore:

```text
Risk Indicator â‰  Confirmed Fraud
