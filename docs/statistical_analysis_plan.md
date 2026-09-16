# Statistical Analysis Plan

## Methods used
- **Mean absolute percent error, max absolute percent error** — for PK numeric
  validation cases (Stage 21), computed via `src/validation.py`
- **Plain agreement counts** ("X of N matched") — for DDI severity and renal category
  validation, not converted to a percentage given small N
- **Descriptive summary of the DDI knowledge base** — class distribution (Stage 11:
  High=1, Moderate=2, None=3), reported as counts, not statistically tested

## Methods explicitly NOT used, and why
- **Confidence intervals** on validation error — would require enough cases for the
  interval to be meaningful; not planned unless case count grows substantially
  beyond what Stage 21 is likely to produce
- **t-tests / significance testing** — same reasoning; testing significance on a
  handful of cases would produce a technically-computable but practically
  meaningless p-value, which is a more sophisticated-looking version of the same
  overclaiming problem addressed at Stage 11/12
- **ROC-AUC / PR-AUC / precision / recall for the ML component** — ruled out at
  Stage 11 due to the singleton High class; unchanged here
- **Correlation analysis** — no paired continuous variables in this project's
  design that would call for it

## Principle
Every statistical claim in the paper should be traceable to a method appropriate
for the actual sample size available, not selected because it is standard practice
in larger studies. Where a standard method doesn't apply due to small N, the paper
states that explicitly rather than omitting the caveat.
