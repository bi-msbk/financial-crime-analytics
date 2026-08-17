# Project Risks

The following risks may affect the quality, scope, analytical validity or business usefulness of the project.

| ID | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| R-001 | Synthetic data may not fully represent real banking behaviour | Medium | High | Clearly document the synthetic nature, assumptions and limitations of the dataset |
| R-002 | Fraud data may be highly imbalanced | High | High | Use appropriate evaluation metrics such as precision, recall, F1 and PR-AUC |
| R-003 | False-positive volumes may overwhelm investigators | High | High | Evaluate alert volumes, precision, alert conversion and investigation workload |
| R-004 | Fraud indicators or models may be difficult to explain | Medium | High | Prefer interpretable features and document the logic behind analytical indicators |
| R-005 | Data-quality issues may affect analytical results | Medium | High | Define and execute data-quality checks before analytical modelling |
| R-006 | Project scope may become too large | High | Medium | Use defined project phases and stage gates to control scope |
| R-007 | Dashboards may become overly complex | Medium | Medium | Design dashboards around stakeholder decisions and prioritise actionable KPIs |
| R-008 | Historical fraud labels may contain classification errors | Medium | High | Perform fraud-label quality checks and document potential limitations |
| R-009 | Simplified fraud rules may not represent real production controls | Medium | High | Clearly document rule assumptions and treat control results as analytical simulation |
| R-010 | Model performance may not generalise beyond the synthetic dataset | Medium | High | Use appropriate validation and clearly state that model results are portfolio-project results |
