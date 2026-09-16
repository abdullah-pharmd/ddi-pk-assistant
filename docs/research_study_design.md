# Research Study Design

## Research objective
To design, implement, and validate a patient-specific clinical decision-support
prototype integrating pharmacokinetic dosing, renal-function-based dose adjustment,
and drug-drug interaction risk assessment for a defined four-drug set (gentamicin,
vancomycin, phenytoin, digoxin), and to evaluate the tool's calculated outputs against
literature-reported reference cases.

## Research question
Does a rule-based/ML-hybrid architecture that integrates renal function,
pharmacokinetic calculation, and drug-interaction assessment produce outputs
consistent with literature-derived reference values, for a small, fully-sourced set
of clinically significant drugs?

**Explicitly not claimed:** clinical outcome improvement, generalization beyond the
four drugs, or superiority over existing DDI checkers.

## Hypothesis
Deterministic PK/renal calculations will show close numerical agreement (small %
error) with literature reference cases, since they implement the same published
equations directly. The ML-based DDI severity classification is NOT hypothesis-tested
for generalization — per `ml_component_design.md`, it is evaluated only as an internal
audit of consistency with its own training data.

## Dataset
- PK/renal reference data: `pk_reference_values.csv` — literature-sourced equations
  and population parameters, 4 drugs
- DDI knowledge base: `ddi_knowledge_base.csv` — 6 sourced drug pairs
- Validation cases: `validation_cases.csv` — literature worked examples, IN PROGRESS

## Inclusion criteria (validation cases)
- Adult patients (population PK parameters used throughout are adult-specific)
- Cases reporting the input parameters needed to run the tool's equations, plus a
  reported result to compare against
- Cases with a traceable citation

## Exclusion criteria
- Pediatric cases
- Hemodialysis or rapidly changing renal function (outside every drug's stated
  validity range)
- Cases relying on drugs outside the four-drug set

## Feature engineering
Fixed at Stage 11: `interaction_category`, `interaction_type`, pathway signal,
`evidence_level`. Target-leakage risk (Stage 12) to be checked when features are
finalized in code.

## Model development
Random Forest, fixed conservative hyperparameters, trained on the full 6-row KB — no
train/test split, explicitly justified rather than hidden (`ml_component_design.md`).

## Validation
Per `validation_framework.md`: percent error for PK numerics, match/mismatch counts
for categorical outputs. No ROC/precision-recall given expected case counts.

## Statistical analysis
Descriptive only: mean/max absolute percent error, plain agreement counts. No
inferential statistics planned unless case count grows enough to support them —
forcing significance testing onto a handful of cases would repeat the overclaiming
Stage 22 guarded against.

## Error analysis
For any case with meaningful error, source of error categorized: genuine tool
limitation vs. differing source assumptions vs. input/transcription error — not
reported as a bare number.

## Limitations
- 4-drug, 6-pair scope only
- ML component is an audit tool, not a validated predictor
- DDI severity adjustment for patient renal status is qualitative, not a sourced
  graded rule
- Drug-specific obesity-adjusted Vd corrections not yet implemented in code (flagged
  gap from Stage 18)
- Validation case count likely small
- Hepatic impairment is a caution flag only, not calculated

## Ethical considerations
- No real patient data used anywhere in this project — synthetic data explicitly
  flagged where used; real cases only from published literature
- Tool explicitly labeled throughout as an educational/research prototype, not for
  clinical use
- No claim of clinical validation is made anywhere in outputs
