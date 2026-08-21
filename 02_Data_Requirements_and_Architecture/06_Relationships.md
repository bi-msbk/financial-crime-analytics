# Data Relationships

## Purpose

This document defines the business and analytical relationships between the entities used by the Financial Crime Analytics & Fraud Detection Platform.

The relationships are aligned with the approved Data Model and Data Dictionary.

---

## 1. Customer â†’ Account

### Business Relationship

One customer may have one or more accounts.

### Cardinality

`Customer 1 : N Account`

### Analytical Relationship

```text
dim_customer.customer_key
        â†“
dim_account.customer_key
