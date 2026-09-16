"""
Module 6 — TDM Interpretation
Ranges sourced in pk_reference_values.csv. Only runs for the four drugs in this
project's scope, all of which are clinically standard TDM drugs.
"""

THERAPEUTIC_RANGES = {
    "gentamicin": {"peak_min": 5.0, "peak_max": 10.0, "trough_max": 2.0, "unit": "ug/mL"},
    "vancomycin": {"auc_min": 400.0, "auc_max": 600.0, "unit": "mg.hr/L (AUC/MIC>=400, primary model)"},
    "phenytoin": {"total_min": 10.0, "total_max": 20.0, "free_min": 1.0, "free_max": 2.0, "unit": "ug/mL"},
    "digoxin": {"min": 0.5, "max": 1.0, "unit": "ng/mL"},
}


def interpret_tdm(drug: str, measured_value: float) -> dict:
    """
    Compares a measured/estimated level to the drug's sourced therapeutic range.
    Returns a qualitative flag only — does NOT auto-recalculate a new dose; a
    human clinician decides the actual adjustment.
    """
    drug_key = drug.strip().lower()
    if drug_key not in THERAPEUTIC_RANGES:
        raise ValueError(f"TDM not defined for '{drug}' in this project's scope")
    rng = THERAPEUTIC_RANGES[drug_key]

    if drug_key == "digoxin":
        low, high = rng["min"], rng["max"]
    elif drug_key == "vancomycin":
        low, high = rng["auc_min"], rng["auc_max"]
    elif drug_key == "gentamicin":
        low, high = rng["trough_max"] * 0, rng["trough_max"]  # trough-below check only
    else:  # phenytoin, total level
        low, high = rng["total_min"], rng["total_max"]

    if measured_value < low:
        status = "below range"
    elif measured_value > high:
        status = "above range"
    else:
        status = "within range"

    return {
        "drug": drug, "measured_value": measured_value,
        "range": rng, "status": status,
        "note": "Qualitative flag only — a human clinician determines any actual "
                "dose change.",
    }
