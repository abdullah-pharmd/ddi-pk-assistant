# Clinical Risk Categorization Design

## Framework (locked)
Three tiers, sourced directly from `ddi_knowledge_base.csv`'s `severity` field, itself
sourced per-pair to a specific citation (per `data_sources_policy.md`):
- **High**
- **Moderate**
- **None**

No finer-grained tiers (e.g., a numeric 1-10 score, or a "Critical" tier above High)
are introduced. Adding granularity beyond what the cited sources actually state would
constitute inventing a clinical claim, which the project's core safety requirement
(Stage 1) and sourcing policy (Stage 6) both rule out. Three categories is the correct
amount of precision for what is currently documented.

## Clinical severity vs. model output — structurally separated

| | Clinical severity | Model output (ML/SHAP) |
|---|---|---|
| Source | Literature (KB lookup, Module 3 rule-based side) | Random Forest fit on the KB (Module 3 ML side) |
| Represents | What the cited sources say about this pair | Whether the model's fit agrees with that label, given KB features |
| Displayed as | Primary/headline field | Supplementary audit panel (per `shap_explainability_design.md`) |
| Scope | As broad as the citation supports | Explicitly scoped to the 6-row dataset only |

This separation is a direct implementation of the original project requirement to
"clearly distinguish clinical severity from model probability" -- carried through into
UI copy (Stage 18), not just internal documentation.

## Traceability check
No new thresholds are introduced at this stage. Severity values and their citations
were already established in Stage 5 (data strategy) and Stage 10 (DDI engine design).
This stage formalizes and confirms that decision rather than introducing new sourcing
work -- a deliberate checkpoint to confirm nothing ungrounded has slipped into the
categorization scheme.
