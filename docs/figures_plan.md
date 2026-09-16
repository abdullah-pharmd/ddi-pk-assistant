# Figures for the Paper

## Figures that are ready to produce now (real content exists)
1. **System architecture diagram** — from `module_design.md`'s data-flow diagram
   (Stage 3), redrawn cleanly for publication
2. **Workflow diagram** — patient input through to report export, following
   app.py's actual tab structure (Stage 18-20)
3. **DDI knowledge base composition** — simple bar chart of severity class counts
   (High=1, Moderate=2, None=3) — descriptive, not a performance figure
4. **SHAP summary plot** — global feature importance from the fitted model on the
   6-row KB, captioned per Stage 13's wording rules (scoped explicitly to this
   dataset)
5. **Example patient explanation** — one SHAP waterfall plot for a specific pair
   (e.g., Vancomycin+Gentamicin), same captioning discipline

## Figures that require Stage 21 to complete first (not yet producible)
6. **PK prediction vs. reference values** — scatter or bar comparison of
   calculated vs. literature-reported values, per validation case — BLOCKED until
   real validation cases exist
7. **Error distribution** — histogram/summary of percent errors across validation
   cases — BLOCKED, same reason

## Figures explicitly NOT included, and why
- **ROC curve, precision-recall curve, confusion matrix as "performance" figures**
  — would misrepresent the ML component's honestly-scoped audit role (Stage 11/12)
  as validated predictive performance. A confusion matrix MAY appear, but only if
  explicitly labeled "training-set fit, not test performance," per
  `model_validation_design.md`

## Note on necessity
Not every figure listed in the original project brief is included. Per the brief's
own instruction to "explain which figures are actually necessary" — figures 6 and 7
are the ones that actually demonstrate the paper's core validation claim; 1-5 support
the architecture and explainability narrative. A figure is included only if it shows
something the text can't convey as clearly, consistent with this project's broader
discipline against padding for appearance's sake.
