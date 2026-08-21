# Investigation Simulation Logic

## Purpose

This document defines the synthetic investigation process used to simulate the operational handling of fraud alerts and suspicious activity.

The investigation dataset shall support:

- Investigation prioritisation.
- High-risk case analysis.
- Open-case analysis.
- Investigation duration analysis.
- Case outcome analysis.

---

## 1. Investigation Model

Investigations shall be generated from fraud alerts and suspicious transactions according to configurable case-creation rules.

Conceptually:

```text
Fraud Alert
      â†“
Case Creation
      â†“
Investigation Priority
      â†“
Investigation
      â†“
Case Outcome
