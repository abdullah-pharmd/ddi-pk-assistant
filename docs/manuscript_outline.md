# Manuscript Outline

## 1. Title
See `paper_titles.md` (Stage 27)

## 2. Abstract
Drafted only once Stage 21's validation results exist — an abstract with placeholder
results would violate the project's no-fabricated-results rule. Structure ready:
background (1-2 sentences) -> objective (from `research_study_design.md`) -> methods
(1-2 sentences) -> key validation results (PENDING Stage 21) -> conclusion, scoped to
match Stage 22's honest novelty verdict.

## 3. Keywords
Pharmacokinetics; drug-drug interactions; clinical decision support; explainable AI;
therapeutic drug monitoring; renal dose adjustment

## 4. Introduction
- Clinical problem: PK dosing + DDI risk + renal adjustment are usually handled by
  separate tools
- Gap: most DDI checkers don't incorporate patient renal function; most PK
  calculators don't cross-reference concurrent DDIs (per `research_novelty_assessment.md`)
- Objective: state plainly from `research_study_design.md` — no overclaiming

## 5. Materials and Methods
- 5.1 System Architecture — from `module_design.md`
- 5.2 Data Sources — from `data_sources_policy.md` and `data_strategy.md`
- 5.3 DDI Engine — from `ddi_engine_design.md`
- 5.4 Pharmacokinetic Engine — from all Stage 8 equation derivations, both linear
  and nonlinear (phenytoin) paths
- 5.5 Machine Learning Component — from `ml_component_design.md`, WITH the honest
  small-N framing stated explicitly, not softened
- 5.6 Explainability — from `shap_explainability_design.md`
- 5.7 Validation Methodology — from `validation_framework.md`

## 6. Results
- 6.1 PK/Renal Validation Results — PENDING Stage 21 real cases
- 6.2 DDI Knowledge Base Composition — descriptive, ready now
- 6.3 ML Component Audit Results — descriptive fit + majority baseline (Stage 12),
  ready now, correctly framed as non-generalizing

## 7. Discussion
- Interpretation of validation results (pending Stage 21)
- Novelty claim, stated at the scope established in `research_novelty_assessment.md`
- Comparison to existing DDI/PK tools (qualitative, not a performance claim)

## 8. Limitations
Direct copy from `research_study_design.md`'s Limitations section — do not soften
or omit any item when drafting the actual manuscript text

## 9. Conclusion
Should not claim more than Results supports — cross-check against Section 6 before
finalizing

## 10. References
Compiled from every citation across `docs/` and `data/*.csv` — full reference list,
not just illustrative examples

## Status
Sections 1, 2, 6.1, 7 (partially) cannot be finalized until Stage 21 produces real
validation results. All other sections have real source material ready to draft from.
