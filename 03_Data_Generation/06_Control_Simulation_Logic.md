
---

# 3.6 `06_Control_Simulation_Logic.md`

```markdown
# Control Simulation Logic

## Purpose

This document defines the synthetic fraud-monitoring controls used to evaluate fraud detection effectiveness.

The control simulation shall support analysis of:

- Detection rate.
- Missed fraud rate.
- False-positive rate.
- Alert conversion rate.
- Control gaps.
- Rule-level effectiveness.

---

## 1. Control Model

Each fraud-monitoring control is represented in:

`dim_fraud_rule`

Each generated alert is represented in:

`fact_fraud_alert`

---

## 2. Control Categories

Rules shall cover indicators such as:

- High transaction amount.
- High transaction velocity.
- New device.
- Geographic anomaly.
- Unusual transaction timing.
- Suspicious merchant activity.
- Behavioural deviation.

---

## 3. Rule Evaluation

Each transaction shall be evaluated against applicable rules.

A rule may:

- Generate an alert.
- Not generate an alert.
- Generate a false-positive alert.
- Detect confirmed fraud.
- Miss confirmed fraud.

---

## 4. Multiple Alerts

A transaction may generate:

- Zero alerts.
- One alert.
- Multiple alerts.

This reflects the approved relationship:

`Transaction 1 : 0..N Fraud Alert`

---

## 5. True Positives

A true-positive alert occurs when:

- The alert is generated.
- The underlying transaction is confirmed fraudulent.

---

## 6. False Positives

A false-positive alert occurs when:

- The alert is generated.
- The underlying transaction is not confirmed fraudulent.

False positives are required for control-effectiveness analysis.

---

## 7. Missed Fraud

Missed fraud occurs when:

- A transaction is confirmed fraudulent.
- No applicable control detects the transaction.

The generated dataset shall contain some missed fraud.

---

## 8. Control Effectiveness

Control performance shall support calculation of:

- Detection rate.
- Missed fraud rate.
- False-positive rate.
- Alert conversion rate.
- Rule-level performance.

---

## 9. Imperfect Controls

Controls shall have different effectiveness levels.

No single rule shall detect all fraud.

This ensures the dataset supports meaningful control-gap analysis.

---

## 10. Alert Output

Each generated alert shall contain:

- alert_id
- transaction_id
- rule_id
- alert_timestamp
- alert_status
- alert_outcome
- confirmed_fraud_flag

The output shall conform to the Step 2 Data Dictionary and Data Grain.
