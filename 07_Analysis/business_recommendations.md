# Business Recommendations

## 1. Executive Recommendation

The primary recommendation is to move from a broad fraud-detection approach toward a more risk-based operating model.

The analysis shows that the current simulated control achieves strong fraud detection coverage at 96.08%, but precision is only 26.71%. This creates substantial false-positive workload while investigations also have a 31.14% open-case rate.

The priority should therefore be to preserve strong detection coverage while improving alert precision, risk segmentation and investigation prioritisation.

---

## 2. Prioritise Digital and Transfer Risk

### Evidence

Mobile and Online channels have the highest observed fraud rates:

- Mobile: 2.20%
- Online: 2.17%
- Card Present: 0.67%
- ATM: 0.66%
- Branch: 0.63%

The highest-risk combination is Mobile + Transfer at 4.00%, followed by Online + Transfer at 3.87%.

### Action

Introduce stronger risk-based monitoring for digital transfer activity.

Potential controls include:

- enhanced transaction monitoring
- contextual risk scoring
- velocity checks
- device and behavioural signals
- geographic consistency checks
- step-up review for higher-risk transactions

### Rationale

The analysis identifies digital transfer activity as a concentrated area of simulated fraud risk.

### Expected impact

Investigation and monitoring resources can be concentrated on higher-risk transaction combinations rather than applying equally aggressive controls across all channels.

---

## 3. Optimise Low-Precision Rules

### Evidence

Rule precision varies substantially:

| Rule | Alerts | Precision |
|---|---:|---:|
| RULE007 | 19,868 | 100.00% |
| RULE001 | 11,155 | 90.21% |
| RULE002 | 21,562 | 78.87% |
| RULE003 | 81,187 | 20.67% |
| RULE005 | 10,678 | 10.21% |

RULE003 generates the largest alert volume while achieving only 20.67% precision.

RULE005 has even lower precision at 10.21%.

### Action

Prioritise RULE003 and RULE005 for rule tuning.

Potential approaches include:

- threshold adjustment
- additional contextual conditions
- customer-risk segmentation
- transaction-type segmentation
- rule combination
- behavioural enrichment
- alert severity differentiation

### Rationale

High-volume, low-precision rules can consume investigation capacity without producing equivalent fraud-detection value.

### Expected impact

Improved precision should reduce unnecessary investigation activity while retaining useful fraud signals.

Any rule changes should be tested against detection coverage to avoid increasing false negatives.

---

## 4. Reduce False-Positive Workload

### Evidence

The simulated control produces:

- 28,825 true positives
- 79,080 false positives
- 1,175 false negatives
- 1,890,920 true negatives

Overall detection rate is 96.08%, while precision is 26.71%.

### Action

Adopt a risk-based alert prioritisation framework rather than treating all alerts equally.

Alerts could be segmented into:

- Critical
- High
- Medium
- Low

based on combined transaction, customer, channel, behavioural and rule-level risk.

### Rationale

The control already captures most fraudulent transactions. The larger optimisation opportunity is therefore improving the quality and prioritisation of alerts.

### Expected impact

Reducing unnecessary alerts should allow investigators to spend more time on genuinely suspicious activity.

This could also reduce investigation backlogs and improve operational efficiency.

---

## 5. Strengthen Customer-Level Risk Segmentation

### Evidence

The Top 1% customer segment contains approximately 363 customers but accounts for 8.18% of total simulated fraud loss.

The broader concentration analysis shows that fraud loss is not evenly distributed across customers.

### Action

Introduce customer-level risk segmentation using factors such as:

- historical transaction behaviour
- transaction value
- fraud history
- device changes
- geographic behaviour
- channel usage
- transaction velocity
- behavioural deviation

### Rationale

Customer-level context can help distinguish isolated unusual transactions from broader changes in customer behaviour.

### Expected impact

Customer risk profiles can support more targeted monitoring and reduce unnecessary intervention for consistently low-risk customers.

---

## 6. Improve Investigation Prioritisation

### Evidence

The investigation population contains:

- 144,450 total cases
- 99,465 closed cases
- 44,985 open cases
- 68.86% closure rate
- 31.14% open-case rate
- 5.08 hours average investigation duration

### Action

Implement risk-based investigation queues.

High-risk alerts should receive priority based on:

1. fraud-risk score
2. transaction value
3. customer risk
4. channel and transaction type
5. rule severity
6. behavioural or geographic anomalies

### Rationale

A large open-case population increases the importance of prioritisation.

Investigators should focus first on cases with the greatest potential financial and customer impact.

### Expected impact

Better prioritisation should improve the allocation of investigation capacity and reduce the likelihood that high-risk cases remain unresolved behind lower-value alerts.

---

## 7. Preserve High-Performing Detection Rules

### Evidence

RULE007 achieves 100% precision and RULE001 achieves 90.21% precision within the simulated evaluation.

### Action

Retain these rules as strong detection components while evaluating whether their underlying signals can be incorporated into broader risk scoring.

### Rationale

Optimisation should not focus exclusively on reducing alert volume.

High-performing controls should be protected from unnecessary weakening.

### Expected impact

The organisation can pursue better precision while preserving effective fraud-detection signals.

---

## 8. Recommended Target State

The recommended target operating model is a layered risk-based fraud-monitoring framework:

```text
Transaction
     |
     v
Transaction-level controls
     |
     v
Channel + transaction-type risk
     |
     v
Customer risk profile
     |
     v
Behavioural / device / geographic signals
     |
     v
Risk score
     |
     v
Alert prioritisation
     |
     v
Investigation
     |
     v
Confirmed outcome
     |
     v
Feedback into controls
