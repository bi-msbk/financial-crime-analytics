| ID    | Risk                                                              | Probability | Impact | Mitigation   |
| ----- | ----------------------------------------------------------------- | ----------- | ------ | ------------ |
| R-001 | Synthetic data may not perfectly represent real banking behaviour | Medium      | High   | Clearly document assumptions |
| R-002 | Fraud data may be highly imbalanced                               | High  | High   | Use precision, recall, PR-AUC and appropriate sampling   |
| R-003 | False positives may overwhelm investigators                       | High  | High   | Measure alert volumes and precision                      |
| R-004 | Model may be difficult to explain                                 | Medium| High   | Use interpretable features and explainability techniques |
| R-005 | Data quality issues may affect analysis                           | Medium| High | Implement data-quality framework    |
| R-006 | Scope may become too large                                        | High  | Medium | Maintain stage gates              |
| R-007 | Dashboard may become overly complex                               | Medium| Medium | Design around business decisions  |
| R-008 | Historical fraud labels may contain classification errors         | Medium| High   | Perform label-quality validation  |
