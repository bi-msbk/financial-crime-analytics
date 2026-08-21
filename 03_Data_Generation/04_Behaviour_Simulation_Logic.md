# Behaviour Simulation Logic

## Purpose

This document defines how realistic customer and transaction behaviour will be simulated before fraud scenarios are introduced.

The objective is to establish credible customer baselines so that fraud can be modelled as behavioural deviation rather than random labelling.

---

## 1. Behavioural Simulation Principle

The generation process shall first establish legitimate transaction behaviour.

Fraud scenarios shall subsequently introduce deviations from these baselines.

This approach supports:

- Customer behavioural analysis.
- Anomaly detection.
- Transaction velocity analysis.
- Unusual-device analysis.
- Geographic anomaly analysis.
- Behavioural deviation analysis.

---

## 2. Customer Behaviour Profiles

Each customer shall receive a behavioural profile based on synthetic characteristics.

The profile may include:

- Expected transaction frequency.
- Typical transaction amount.
- Preferred transaction channels.
- Preferred transaction types.
- Preferred merchant categories.
- Normal geographic regions.
- Normal device usage.
- Typical transaction times.

---

## 3. Transaction Frequency

Transaction frequency shall vary across customers.

The generated population shall include:

- Low-frequency customers.
- Typical-frequency customers.
- High-frequency customers.

Frequency shall not be identical across customers.

---

## 4. Transaction Amount

Transaction amounts shall contain realistic variation.

The distribution shall include:

- Lower-value routine transactions.
- Medium-value transactions.
- Higher-value transactions.
- A small number of unusually high-value transactions.

Transaction amounts shall not be uniformly distributed.

---

## 5. Channel Behaviour

Customers shall have differing channel preferences, including where applicable:

- Online.
- Mobile.
- Card-present.
- ATM.
- Branch or other supported channels.

Channel behaviour shall vary by customer profile.

---

## 6. Merchant Behaviour

Customers shall have preferred merchant categories.

Examples include:

- Retail.
- Groceries.
- Travel.
- Hospitality.
- Utilities.
- Digital services.
- Entertainment.

Merchant behaviour shall contain both repeated and occasional activity.

---

## 7. Device Behaviour

Customers shall normally reuse previously observed devices.

New devices shall occur naturally but shall be less common than established devices.

This provides a baseline for the previously unseen device fraud indicator.

---

## 8. Geographic Behaviour

Customers shall normally transact within expected geographic areas.

A smaller proportion of transactions may occur outside the normal customer region.

This provides a baseline for geographic anomaly analysis.

---

## 9. Temporal Behaviour

Transaction behaviour shall vary by:

- Hour of day.
- Day of week.
- Weekend.
- Month.
- Seasonal periods.

The dataset shall contain realistic temporal variation rather than identical activity across all time periods.

---

## 10. Behavioural Baseline

Customer-level baselines shall support calculation of indicators such as:

- Amount deviation.
- Frequency deviation.
- Velocity deviation.
- New-device indicator.
- Geographic deviation.
- Channel deviation.
- Merchant-category deviation.
- Time-of-day deviation.

---

## 11. Fraud Handover

The behavioural simulation output shall become the input to:

`04_Fraud_Simulation_Logic.md`

Fraud scenarios shall modify or extend selected behavioural patterns without making fraud perfectly deterministic.
