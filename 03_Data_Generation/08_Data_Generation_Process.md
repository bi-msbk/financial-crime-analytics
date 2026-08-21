
---

# 3.8 `08_Data_Generation_Process.md`

```markdown
# Data Generation Process

## Purpose

This document defines the end-to-end execution process for generating the synthetic analytical dataset.

The process shall be deterministic when executed with the same configuration, code version and random seed.

---

## 1. Generation Workflow

```text
Load Configuration
      â†“
Set Random Seed
      â†“
Generate Geography
      â†“
Generate Date
      â†“
Generate Customers
      â†“
Generate Accounts
      â†“
Generate Merchants
      â†“
Generate Devices
      â†“
Generate Fraud Rules
      â†“
Generate Customer Behaviour Profiles
      â†“
Generate Legitimate Transactions
      â†“
Inject Fraud Scenarios
      â†“
Generate Fraud Outcomes
      â†“
Evaluate Fraud Rules
      â†“
Generate Fraud Alerts
      â†“
Generate Investigation Cases
      â†“
Run Validation
      â†“
Write Final Datasets
      â†“
Write Metadata
      â†“
Generate Summary
