"""
Module 2 — Renal Function
Source: Cockcroft DW, Gault MH. Nephron. 1976;16(1):31-41. (CrCl equation)
        FDA Guidance for Industry, "Pharmacokinetics in Patients with Impaired
        Renal Function," Table 1, p.7. (category thresholds)
        Bauer LA, Applied Clinical Pharmacokinetics, 2nd ed., Ch.3 p.56 (weight rule)
        Winter M, Basic Clinical Pharmacokinetics, 6th ed., Ch.3 p.104-105 Eq.3.9
"""


def calculate_ibw(height_cm: float, sex: str) -> float:
    """Ideal body weight, Devine formula (kg)."""
    if height_cm <= 0:
        raise ValueError("height_cm must be positive")
    if sex not in ("male", "female"):
        raise ValueError("sex must be 'male' or 'female'")
    height_in = height_cm / 2.54
    inches_over_5ft = max(height_in - 60, 0)
    return (50.0 if sex == "male" else 45.5) + 2.3 * inches_over_5ft


def crcl_cockcroft_gault(age: int, actual_weight_kg: float, height_cm: float,
                          sex: str, scr_mg_dl: float) -> dict:
    """
    Cockcroft-Gault CrCl with obesity-aware weight selection.
    Source: Cockcroft DW, Gault MH. Nephron. 1976;16(1):31-41.
    NOT valid in acute kidney injury (unstable SCr) or extremes of muscle mass.
    """
    if age <= 0 or age > 130:
        raise ValueError("age must be a plausible positive value")
    if actual_weight_kg <= 0:
        raise ValueError("actual_weight_kg must be positive")
    if scr_mg_dl <= 0:
        raise ValueError("scr_mg_dl must be positive (division by zero otherwise)")
    if sex not in ("male", "female"):
        raise ValueError("sex must be 'male' or 'female'")

    ibw = calculate_ibw(height_cm, sex)
    if actual_weight_kg <= ibw:
        weight_used, weight_basis = actual_weight_kg, "actual (below IBW)"
    elif actual_weight_kg <= 1.3 * ibw:
        weight_used, weight_basis = ibw, "IBW"
    else:
        weight_used = ibw + 0.4 * (actual_weight_kg - ibw)
        weight_basis = "adjusted body weight (obesity correction)"

    sex_factor = 0.85 if sex == "female" else 1.0
    crcl = ((140 - age) * weight_used * sex_factor) / (72 * scr_mg_dl)
    return {
        "crcl_ml_min": round(crcl, 1),
        "weight_used_kg": round(weight_used, 1),
        "weight_basis": weight_basis,
        "reference": "Cockcroft DW, Gault MH. Nephron. 1976;16(1):31-41.",
    }


def renal_category(crcl_ml_min: float) -> dict:
    """
    Categorize CrCl per FDA renal-impairment dosing guidance thresholds.
    Source: FDA Guidance for Industry, "Pharmacokinetics in Patients with Impaired
    Renal Function," Table 1, p.7.
    Used for Module 5's categorical dose-adjustment logic only -- each drug's own
    clearance equation (Module 4) uses continuous CrCl directly, not this category.
    """
    if crcl_ml_min < 0:
        raise ValueError("crcl_ml_min cannot be negative")
    if crcl_ml_min >= 90:
        category = "Normal"
    elif crcl_ml_min >= 60:
        category = "Mild"
    elif crcl_ml_min >= 30:
        category = "Moderate"
    else:
        category = "Severe"
    return {
        "category": category,
        "crcl_ml_min": crcl_ml_min,
        "reference": "FDA Guidance for Industry, Pharmacokinetics in Patients with "
                      "Impaired Renal Function, Table 1, p.7",
    }
