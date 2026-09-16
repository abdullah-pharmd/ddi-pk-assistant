# Model Validation Design

## v1 — what is actually reported (descriptive only, n=6, singleton High class)
- Confusion matrix from a full-data fit, explicitly labeled "training-set fit," never
  "test performance"
- Majority-class baseline for honest comparison: always predicting "None" (the most
  common label) achieves 3/6 = 50% by construction, using no information at all -- any
  reported fit should be discussed against this number, not presented in isolation
- SHAP explanations of the fitted model's feature-severity associations -- legitimate
  at this scale, since it explains the model's relationship to KNOWN data, not its
  ability to generalize to unseen pairs

## v1 — explicitly NOT reported
- Accuracy / precision / recall / F1 / ROC-AUC / PR-AUC framed as performance metrics
- Any cross-validation result -- LOOCV is structurally uninformative here because the
  High class has n=1 (Stage 11); removing the sole High example from training
  guarantees that fold fails regardless of model quality
- Any language implying validated generalization beyond this specific 6-pair dataset

## Known current risk: target leakage
`interaction_present` and `interaction_category` are close to definitionally tied to
`severity=None` in the current 6-row KB (a None severity essentially requires
interaction_present=NO). If Stage 11's features are implemented without care, the
model could trivially "solve" the None class by keying off this near-tautological
relationship rather than learning anything about mechanism/pathway/evidence-level.
Flagged now so it is addressed deliberately when `src/prediction.py` is actually
written, not discovered after the fact.

## v2 framework (documented now for methodological credibility; applied once the
## knowledge base is expanded per Stage 11's Future Work path)

| Concept | Why it matters | Trigger condition |
|---|---|---|
| Train/test split or stratified k-fold | Estimates generalization to unseen pairs | Enough rows per class for a defensible split |
| Accuracy alone is insufficient | A model can score well by always predicting the majority class (see 50% baseline above) | Always true, not v2-specific |
| Precision/Recall/F1 per class | Reveals whether rare-but-important classes (e.g. High severity) are being missed | Once class counts support per-class evaluation |
| ROC-AUC / PR-AUC | Threshold-independent separability view; PR-AUC more informative under imbalance | Once minority class has enough examples |
| Data leakage (general) | Features that indirectly encode the answer | Check at any dataset size, every time features change |
| Target leakage (specific, current risk) | `interaction_present`/`interaction_category` near-tautological with `severity=None` currently | Address when features are implemented in code |
| Synthetic-data leakage | Synthetic and real rows must not be split across train/test such that a synthetic near-duplicate leaks a real row's answer | Only relevant if synthetic patient-context augmentation is ever justified by a sourced escalation rule (currently rejected, Stage 11) |

## Reporting principle carried through both versions
Every validation statement in this project states its own scope explicitly --
"consistent with the small, fully-sourced v1 dataset" or "pending KB expansion for v2"
-- rather than letting a reader infer a broader claim than the data supports.
