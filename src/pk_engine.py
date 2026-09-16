"""
Module 4 — Pharmacokinetic Engine
Two paths: linear/first-order (gentamicin, vancomycin, digoxin) and
nonlinear/Michaelis-Menten (phenytoin). See docs/drug_selection.md for rationale.

Weight-basis corrections: per pk_reference_values.csv's "General obesity trigger
threshold" row, the drug-specific corrected weight formula ONLY applies when
actual weight exceeds IBW by >30% (obesity trigger) -- otherwise, ACTUAL weight is
used directly. An earlier draft of this file applied the corrected formula
unconditionally, which broke the Stage 21 validation cases (patient was not obese,
so actual weight was the correct basis) -- caught and fixed before this was shipped.
"""
from renal import calculate_ibw


def _weight_basis(actual_weight_kg: float, ibw: float, obese_formula) -> float:
    """Applies the >30%-over-IBW obesity trigger uniformly across drugs."""
    if actual_weight_kg > 1.3 * ibw:
        return obese_formula(actual_weight_kg, ibw)
    return actual_weight_kg


def gentamicin_pk(weight_kg: float, crcl_ml_min: float, height_cm: float, sex: str,
                   cpeak_target: float = 8.0) -> dict:
    """
    Source: Bauer LA, Applied Clinical Pharmacokinetics, 2nd ed.
            ke: p.110, Fig.4-2 p.105. CL=ke x Vd: Table 4-2B, p.114.
            Obesity Vd correction: V=0.26 x [IBW + 0.4(TBW-IBW)], Ch.4 p.108,111,125
            -- applies ONLY when weight_kg >30% over IBW; otherwise Vd=0.26*actual.
    NOT valid for hemodialysis patients (p.162) or rapidly changing renal function.
    KNOWN GAP: obese-patient CrCl should use Salazar-Corcoran equation instead of
    Cockcroft-Gault -- not yet sourced.
    """
    if weight_kg <= 0 or crcl_ml_min < 0:
        raise ValueError("weight_kg must be positive and crcl_ml_min non-negative")
    ibw = calculate_ibw(height_cm, sex)
    weight_for_vd = _weight_basis(weight_kg, ibw, lambda w, i: i + 0.4 * (w - i))
    vd_l = 0.26 * weight_for_vd
    ke = 0.00293 * crcl_ml_min + 0.014
    cl_l_hr = ke * vd_l
    half_life_hr = 0.693 / ke
    loading_dose_mg = cpeak_target * vd_l
    return {
        "vd_l": round(vd_l, 2), "weight_used_for_vd_kg": round(weight_for_vd, 1),
        "ke_per_hr": round(ke, 4), "cl_l_hr": round(cl_l_hr, 2),
        "half_life_hr": round(half_life_hr, 2),
        "loading_dose_mg": round(loading_dose_mg, 1),
        "reference": "Bauer LA, Applied Clinical Pharmacokinetics, 2nd ed., "
                      "ke: p.110/Fig.4-2 p.105; CL=keV: Table 4-2B p.114; "
                      "Obesity Vd correction: Ch.4 p.108,111,125",
    }


def vancomycin_pk(weight_kg: float, crcl_ml_min: float, height_cm: float, sex: str,
                   auc24_target: float = 500.0) -> dict:
    """
    AUC-guided (primary model per data_strategy.md / ASHP-IDSA 2020).
    Source: Bauer LA, Applied Clinical Pharmacokinetics, 2nd ed., Ch.5, p.212/215.
    Bug #1 (Stage 8A): CL equation outputs mL/min, converted to L/hr before use.
    Bug #2 (Stage 21 validation): nonrenal constant scales with weight
    (0.05*weight_kg), not flat +0.05 mL/min -- verified against Bauer Examples 1-2
    (V1: 70kg/CrCl97 -> t1/2=7.98h vs reported 8h; V2: 70kg/CrCl25 -> t1/2=27.11h
    vs reported 27h).
    Weight basis: CLEARANCE uses actual (total) body weight always (kidney
    hypertrophy in obesity, Ch.5 p.212-213). Vd normally uses actual weight too;
    Vd = 0.7 L/kg x IBW ONLY applies if weight is >30% over IBW (obesity
    correction, Ch.5 p.216,229) -- this was verified against Bauer's own worked
    examples, where the patient (70kg actual vs 73kg IBW, NOT obese) used actual
    weight for Vd (49L = 0.7*70), not IBW (which would give 51.1L).
    NOT valid for hemodialysis patients, rapidly changing renal function, or
    >30% over IBW (Matzke Nomogram not valid there per source).
    """
    if weight_kg <= 0 or crcl_ml_min < 0:
        raise ValueError("weight_kg must be positive and crcl_ml_min non-negative")
    ibw = calculate_ibw(height_cm, sex)
    weight_for_vd = _weight_basis(weight_kg, ibw, lambda w, i: i)  # obese -> IBW
    vd_l = 0.7 * weight_for_vd
    cl_ml_min = 0.695 * crcl_ml_min + 0.05 * weight_kg  # CL always uses actual weight
    cl_l_hr = cl_ml_min * 60 / 1000
    k = cl_l_hr / vd_l
    half_life_hr = 0.693 / k
    daily_dose_mg = auc24_target * cl_l_hr
    return {
        "vd_l": round(vd_l, 2), "weight_used_for_vd_kg": round(weight_for_vd, 1),
        "cl_ml_min": round(cl_ml_min, 2), "cl_l_hr": round(cl_l_hr, 2),
        "k_per_hr": round(k, 4), "half_life_hr": round(half_life_hr, 2),
        "daily_dose_mg": round(daily_dose_mg, 0),
        "reference": "Bauer LA, Applied Clinical Pharmacokinetics, 2nd ed., "
                      "Ch.5, Fig.5-2 p.212, p.215; Vd obesity basis: p.212-213,216,229; "
                      "AUC target: Rybak et al. 2020",
    }


def digoxin_pk(weight_kg: float, crcl_ml_min: float, nyha_class: str,
               height_cm: float, sex: str) -> dict:
    """
    Jusko-Koup model, raw CrCl (consistent with Module 2's Cockcroft-Gault).
    Source: Bauer LA, Applied Clinical Pharmacokinetics, 2nd ed., Ch.6, p.305/312.
    ClNR depends on NYHA heart-failure class -- REQUIRED input.
    Weight basis: Vd normally uses actual weight; V=7 L/kg x IBW ONLY applies
    when weight is >30% over IBW (Ch.6 p.312-313,318) -- verified against Bauer's
    own worked example (70kg actual vs 73kg IBW, NOT obese: V=490L=7*70 actual,
    not 7*73=511L IBW).
    NOT valid for rapidly changing renal function.
    """
    if weight_kg <= 0 or crcl_ml_min < 0:
        raise ValueError("weight_kg must be positive and crcl_ml_min non-negative")
    if nyha_class not in ("I", "II", "III", "IV"):
        raise ValueError("nyha_class must be 'I', 'II', 'III', or 'IV'")
    ibw = calculate_ibw(height_cm, sex)
    weight_for_vd = _weight_basis(weight_kg, ibw, lambda w, i: i)  # obese -> IBW
    cl_nr_ml_min = 40.0 if nyha_class in ("I", "II") else 20.0

    vd_l = 7.0 * weight_for_vd
    cl_ml_min = 1.303 * crcl_ml_min + cl_nr_ml_min
    cl_l_hr = cl_ml_min * 60 / 1000
    k = cl_l_hr / vd_l
    half_life_hr = 0.693 / k
    return {
        "vd_l": round(vd_l, 1), "weight_used_for_vd_kg": round(weight_for_vd, 1),
        "cl_ml_min": round(cl_ml_min, 2), "cl_l_hr": round(cl_l_hr, 3),
        "k_per_hr": round(k, 5), "half_life_hr": round(half_life_hr, 1),
        "cl_nr_used": cl_nr_ml_min,
        "reference": "Bauer LA, Applied Clinical Pharmacokinetics, 2nd ed., "
                      "Ch.6, p.305/312 (Jusko-Koup, raw CrCl); Vd obesity basis: p.312-313,318",
    }


def phenytoin_pk(weight_kg: float, css_target_mg_l: float, height_cm: float, sex: str,
                  vmax_mg_kg_day: float = 7.0, km_mg_l: float = 4.0) -> dict:
    """
    Michaelis-Menten (nonlinear) kinetics.
    Source: Richens A, Dunlop A. Lancet. 1975;2(7928):247-248 (equation).
            Population Vmax/Km: Bauer p.501 (also p.20, p.491);
            confirmed in Winter p.398/402.
    Weight basis: Vmax weight term uses actual weight normally; maintenance
    dosing conventionally uses IBW only in obese patients. Vd obesity correction:
    Vd = 0.7 L/kg x [IBW + 1.33(TBW-IBW)], applies only if >30% over IBW
    (Bauer Ch.10 p.492,512).
    NOT valid: non-steady-state levels, or total-level interpretation without
    winter_tozer_correction() when albumin <3.5 g/dL or CrCl <25 mL/min.
    Vmax/Km are POPULATION STARTING ESTIMATES.
    """
    if weight_kg <= 0 or css_target_mg_l <= 0:
        raise ValueError("weight_kg and css_target_mg_l must be positive")
    ibw = calculate_ibw(height_cm, sex)
    weight_for_vmax = _weight_basis(weight_kg, ibw, lambda w, i: i)
    vmax_mg_day = vmax_mg_kg_day * weight_for_vmax
    if css_target_mg_l >= vmax_mg_day:
        raise ValueError("Target concentration implies dose >= Vmax — not achievable")
    dose_mg_day = (vmax_mg_day * css_target_mg_l) / (km_mg_l + css_target_mg_l)

    weight_for_vd = _weight_basis(weight_kg, ibw, lambda w, i: i + 1.33 * (w - i))
    vd_l = 0.7 * weight_for_vd
    return {
        "vmax_mg_day": round(vmax_mg_day, 0), "km_mg_l": km_mg_l,
        "dose_mg_day": round(dose_mg_day, 1), "vd_l": round(vd_l, 1),
        "weight_used_kg": round(weight_for_vmax, 1),
        "reference": "Richens & Dunlop 1975 (equation); "
                      "Bauer p.501, Winter p.398/402 (population Vmax/Km); "
                      "Vd obesity basis: Bauer Ch.10 p.492,512",
    }


def winter_tozer_correction(c_measured_mg_l: float, albumin_g_dl: float,
                             severe_renal_impairment: bool) -> dict:
    """
    Correct total phenytoin level for low albumin (and renal impairment if present).
    Source: Bauer p.489; Winter p.406 Eq.14.2 (normal renal) / p.406-407 Eq.14.3 (CrCl<10).
    Use when albumin < 3.5 g/dL or CrCl < 25 mL/min.
    """
    if c_measured_mg_l <= 0 or albumin_g_dl <= 0:
        raise ValueError("c_measured_mg_l and albumin_g_dl must be positive")
    if severe_renal_impairment:
        c_corrected = c_measured_mg_l / (0.1 * albumin_g_dl + 0.1)
        equation_used = "Eq. 14.3 (CrCl < 10 mL/min) -- Winter p.406-407 / Bauer p.489"
    else:
        c_corrected = c_measured_mg_l / (0.2 * albumin_g_dl + 0.1)
        equation_used = "Eq. 14.2 (CrCl >= 10-25 mL/min) -- Winter p.406 / Bauer p.489"
    return {"c_corrected_mg_l": round(c_corrected, 2), "equation_used": equation_used}
