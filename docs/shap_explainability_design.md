# SHAP Explainability Design (Module 7 — ML side)

## Scope, carried forward from Stage 11/12
SHAP here is an audit tool on a 6-row, fully-sourced dataset, not an explanation of
generalizable predictions. All wording and visualization choices below exist to keep
that distinction visible to the end user, not just documented in `docs/`.

## Global feature importance
SHAP summary plot across all 6 KB rows. Its real value: a diagnostic check on the
model's own fit -- confirming it leans on clinically sensible features
(`interaction_category`, `evidence_level`) rather than the target-leakage risk flagged
in Stage 12 (`interaction_present` being near-tautological with `severity=None`).

## Individual prediction explanation
Waterfall/force plot per pair, showing which features pushed the model toward its
output for that pair. Framed explicitly as "why the model's fit agrees with the
literature-sourced label," not as independent model discovery.

## Visualization
`shap.summary_plot()` (global), `shap.plots.waterfall()` (per-instance) — standard
matplotlib-based SHAP output, embedded in Streamlit at Stage 18.

## Clinical interpretation guardrails
SHAP values reflect statistical association within the fitted model on this specific
6-row dataset -- never clinical causation, never generalization beyond this dataset.
Both points stated in-UI, not just in documentation.

## UI wording rules (locked)
| Never show | Show instead |
|---|---|
| "Model prediction: High risk (94% confidence)" | "This pair's literature-sourced severity is High. Below: which features the model's fit associates with that label." |
| SHAP plot with no framing text | SHAP plot captioned: "Reflects patterns in this project's 6-pair sourced dataset only -- not validated for pairs outside this set." |
| ML output presented as primary severity source | KB literature severity (rule-based lookup) is primary/headline; SHAP is a supplementary "why does the model agree" panel |

## Connection to Module 7's deterministic side
Two structurally and visually separate explanation panels:
- **Deterministic (PK/renal/dose):** Input -> Equation -> Result -> Reference
  (Stage 7's five-step pattern)
- **DDI severity:** Literature severity (primary) -> SHAP audit view (supplementary,
  explicitly scoped)

These render as visually distinct UI panels (Stage 18) so a user cannot mistake a
model's audit-view explanation for a validated prediction, or vice versa.
