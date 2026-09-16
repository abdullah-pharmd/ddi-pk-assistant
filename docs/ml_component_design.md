# ML Component Design (Module 3 — DDI Risk Classification)

## Data reality check (must be stated explicitly in the paper, not glossed over)
`ddi_knowledge_base.csv` has 6 pairs. Severity label distribution:

| Severity | Count |
|---|---|
| High | 1 |
| Moderate | 2 |
| None | 3 |

The High class is a **singleton** (n=1). This means conventional train/test splitting
or k-fold/leave-one-out cross-validation cannot produce a meaningful estimate of
generalization for that class — removing the only High example from training
guarantees that fold fails regardless of model quality. This is a structural property
of the dataset, not a limitation to caveat away.

## Framing decision (locked)
This component is framed as an **explainability/audit demonstration on a small,
fully-sourced dataset** — not a validated predictive classifier. This is consistent
with the framing already committed to in `data_strategy.md` ("closer to structured/
explainable summarization of known rules than discovering new interactions").

This decision was made deliberately in favor of scientific credibility over a more
impressive-sounding but indefensible claim: a reported accuracy/F1/ROC-AUC number on
this dataset would be statistical noise, and presenting it as validated performance
would undermine the project's credibility with any reviewer familiar with small-sample
ML pitfalls — the opposite of the intended effect for a scholarship/publication
submission.

## Rejected alternative: synthetic patient-context augmentation
Considered and rejected. Stage 10 established there is no sourced rule for how patient
factors (e.g., renal status) change severity for these pairs (severity adjustment was
locked as qualitative, not scored). Without a sourced rule to vary labels by, synthetic
patient-context rows would have nothing real to vary the target by — this would amount
to fabricating labeled training data, which the project's data-honesty requirements
(Stage 1, Stage 5) explicitly rule out.

## Target and features
- **Target:** `severity` (High / Moderate / None) — 3-class, from the KB's `severity` field
- **Features**, all KB-derived (not patient-specific, per Stage 10):
  - `interaction_category` (pharmacologic / analytical_interference / none)
  - `interaction_type` (PK / PD / N/A), one-hot encoded
  - `mechanism` presence/pathway signal, extracted as available
  - `evidence_level` (established-guideline-level / established-study-level / N/A)

## Validation approach (honest version)
- Train on the full 6-row dataset
- **No held-out test set, no cross-validation performance claim** — the dataset is too
  small and the class distribution too skewed (singleton class) for either to produce
  an interpretable result
- Report the model's fit on the full training set purely as an **illustration that the
  KB's own features are internally consistent with its own severity labels** — framed
  explicitly as an audit/sanity check, not a generalization claim
- A majority-class baseline (always predict "None," the most common label) is reported
  alongside, so the reader can see what a trivial baseline would produce for comparison

## Model choice
**Random Forest** (or a single shallow decision tree, given SHAP explains either) —
consistent with the AMR Predictor's methodology, and appropriately simple for a
6-row dataset. XGBoost is explicitly NOT used here: its added complexity offers no
benefit at this scale and would look like over-engineering relative to the data.

## Hyperparameters
Minimal, fixed (not tuned): small `n_estimators` (e.g., 50), shallow `max_depth`
(e.g., 2-3) — deliberately conservative given n=6, to avoid any appearance of fitting
to noise.

## What SHAP contributes here
Even without a generalization claim, SHAP is still legitimate and useful: it shows
*why* the model's fit associates certain KB features (e.g., `interaction_category`,
`evidence_level`) with certain severity labels — this is the "explainable audit of a
curated knowledge base" contribution, and is honestly presentable regardless of
dataset size, since it's explaining the model's fit to known data, not predicting
unseen cases.

## Future Work (paper-ready framing for a v2 growth path)
A credible, explicitly-stated next step: expand the DDI knowledge base to additional
pairs using the same sourcing standard (`data_sources_policy.md`), which is what would
be required before a genuine predictive claim (real train/test split, real
cross-validated metrics) becomes statistically defensible. Stating this as a scoped
next step — rather than attempting it prematurely on 6 rows — is itself a point worth
making in the paper's Discussion/Limitations section.
