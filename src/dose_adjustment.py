"""
Module 5 — Dose Adjustment (integration point)
Reads from Module 2 (renal), Module 3 (DDI), Module 6 (TDM), and Module 1's
hepatic flag. This is the only module that converges all four — the concrete
implementation of the project's core cross-domain integration (docs/module_design.md).
Hepatic impairment is a caution FLAG only, never a calculated dose change, per
docs/project_scope.md.
"""


def assess_dose_adjustment(renal_category: str, ddi_findings: list,
                            tdm_status: str = None, hepatic_flag: bool = False) -> dict:
    """
    Aggregates adjustment triggers from all upstream modules. Does not compute a
    new numeric dose itself — that is Module 4's job; this module determines
    WHETHER adjustment is indicated and WHY, citing the responsible module(s).
    """
    reasons = []

    if renal_category in ("Moderate", "Severe"):
        reasons.append(f"renal impairment ({renal_category}) — see Module 4's "
                        f"drug-specific renally-cleared dosing")

    high_severity_ddi = [f for f in ddi_findings
                          if f.get("pair_found_in_kb") and f.get("severity") == "High"]
    if high_severity_ddi:
        pairs = ", ".join(f"{f['drug_a']}+{f['drug_b']}" for f in high_severity_ddi)
        reasons.append(f"high-severity interacting drug(s) present ({pairs}) — "
                        f"see Module 3 for monitoring recommendations")

    if tdm_status in ("above range", "below range"):
        reasons.append(f"measured/estimated concentration is {tdm_status} — "
                        f"clinician judgment required on direction of adjustment")

    if hepatic_flag:
        reasons.append("hepatic impairment flagged — CAUTION ONLY, no calculated "
                        "adjustment provided for this factor (out of scope per "
                        "docs/project_scope.md); clinical correlation required")

    return {
        "adjustment_indicated": len(reasons) > 0,
        "reasons": reasons,
        "note": "This module identifies WHETHER and WHY adjustment may be "
                "indicated. It does not replace clinical judgment, and hepatic "
                "considerations are flagged, not calculated.",
    }
