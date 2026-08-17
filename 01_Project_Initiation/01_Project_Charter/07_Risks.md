# Project Risks

| ID    | Risk                                                              | Probability | Impact | Mitigation |
|-----------------------------------------------------------------------------------------------------------------------------------------|
| R-001 | Synthetic data may not perfectly represent real banking behaviour | Medium      | High | Document assumptions and limitations |
| R-002 | Fraud data may be highly imbalanced                               | High        | High | Use precision, recall, F1 and PR-AUC |
| R-003 | False positives may overwhelm investigators                       | High        | High | Measure alert volume and precision |
| R-004 | Fraud model may be difficult to explain                           | Medium  | High | Use interpretable features and explainability techniques |
| R-005 | Data-quality issues may affect analysis                           | Medium      | High | Implement data-quality controls |
| R-006 | Project scope may become too large                                | High        | Medium | Use defined phase gates |
| R-007 | Dashboard may become overly complex                               | Medium      | Medium | Design around business decisions |
| R-008 | Historical fraud labels may contain classification errors         | Medium      | High | Perform fraud-label validation |