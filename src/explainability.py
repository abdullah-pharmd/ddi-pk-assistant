"""
Module 7 — Explainability
Two structurally separate explanation types, per docs/shap_explainability_design.md:
1. Deterministic equation trace (Input -> Equation -> Result -> Reference)
2. ML SHAP audit panel (supplementary, explicitly scoped to the 6-row KB)
These must render as visually distinct UI sections -- never merged into one
panel, so a user cannot mistake a model's audit-view explanation for a
validated prediction, or vice versa.
"""


def format_equation_trace(result: dict, calculation_name: str) -> dict:
    """
    Formats any deterministic module's result dict into the standard five-step
    trace pattern (Stage 7): Input -> Equation -> Result -> Reference. This is
    NOT a new calculation -- it only reformats an existing result for display.
    """
    reference = result.get("reference", "No reference recorded")
    inputs_and_results = {k: v for k, v in result.items() if k != "reference"}
    return {
        "calculation_name": calculation_name,
        "values": inputs_and_results,
        "reference": reference,
        "panel_type": "deterministic_equation_trace",
    }


def format_shap_audit_panel(shap_values, feature_names, pair_index: int,
                             pair_label: str, predicted_class: str) -> dict:
    """
    Formats a SHAP explanation for one DDI pair as a supplementary AUDIT panel.
    Per docs/shap_explainability_design.md's locked UI wording rules: this is
    NEVER the primary/headline severity source, and always carries the
    dataset-scope caveat.
    """
    return {
        "pair_label": pair_label,
        "predicted_class": predicted_class,
        "feature_names": list(feature_names),
        "panel_type": "ml_shap_audit",
        "caveat": (
            "This reflects patterns in this project's 6-pair sourced dataset "
            "only -- it is NOT validated for pairs outside this set, and does "
            "NOT represent independent model discovery. The literature-sourced "
            "severity above is the primary clinical value; this panel shows "
            "which features the model's fit associates with that label."
        ),
    }
