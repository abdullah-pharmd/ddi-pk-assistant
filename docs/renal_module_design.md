# Renal Function Module Design (Module 2)

## Why CrCl, not eGFR
Every drug-dosing equation sourced in Stage 8 (gentamicin, vancomycin, digoxin) was
built on CrCl, not eGFR (MDRD/CKD-EPI) — eGFR is normalized to 1.73 m² body surface
area and would introduce a units/reference mismatch with those equations. Module 2
outputs raw CrCl only, for direct compatibility with Stage 8's equations.

## Equation — Cockcroft-Gault
```
CrCl (mL/min) = [(140 - age) x weight_kg x (0.85 if female)] / (72 x SCr)
```
Source: Cockcroft DW, Gault MH. Nephron. 1976;16(1):31-41.

## Weight selection rule
Cockcroft-Gault using raw actual body weight overestimates CrCl in obese patients.
This module applies:
- **Actual body weight**, if actual weight <= ideal body weight (IBW)
- **IBW** (Devine formula), if actual weight is up to 30% above IBW
- **Adjusted body weight** = IBW + 0.4 x (actual - IBW), if actual weight exceeds
  IBW by more than 30%

This resolves the obesity/Vd gap flagged during Stage 8A (gentamicin, vancomycin) at
the source — by correcting the weight used in CrCl itself, downstream PK calculations
for all drugs automatically receive a more physiologically appropriate renal-function
input. Note: this does NOT correct each drug's own Vd equation (which still uses a
population-average L/kg figure) — that residual limitation should still be stated in
the eventual Limitations section, not treated as fully resolved by this fix alone.

## Renal impairment categories (for Module 5's dose-adjustment logic)
Source: FDA Guidance for Industry, "Pharmacokinetics in Patients with Impaired Renal
Function — Study Design, Data Analysis, and Impact on Dosing," Table 1, p.7.

| Category | CrCl (mL/min) |
|---|---|
| Normal | >= 90 |
| Mild | 60 - <90 |
| Moderate | 30 - <60 |
| Severe | <30 |

**Note on source conflict, resolved:** Bauer (Applied Clinical Pharmacokinetics, 2nd
ed.) does not define categorical bins — CrCl is used continuously in each drug's
clearance equation. Bauer's own general normal-function threshold (CrCl >80 mL/min,
Ch.3 p.56, referenced again in Ch.4 p.102/Ch.5 p.212/Ch.6 p.305) differs from FDA's
>=90 mL/min cutoff. Decision: use FDA's categorical thresholds for Module 5's
category-based logic, since that is what they are designed for; continue using
Bauer's continuous CrCl directly (uncategorized) inside each drug's own clearance
equation, since binning CrCl before plugging it into a continuous equation would
introduce unnecessary precision loss.

## Python implementation
```python
def calculate_ibw(height_cm: float, sex: str) -> float:
    """Ideal body weight, Devine formula (kg)."""
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
        "crcl_ml_min": round(crcl, 1), "weight_used_kg": round(weight_used, 1),
        "weight_basis": weight_basis,
        "reference": "Cockcroft DW, Gault MH. Nephron. 1976;16(1):31-41."
    }


def renal_category(crcl_ml_min: float) -> dict:
    """
    Categorize CrCl per FDA renal-impairment dosing guidance thresholds.
    Source: FDA Guidance for Industry, "Pharmacokinetics in Patients with Impaired
    Renal Function," Table 1, p.7.
    Used for Module 5's categorical dose-adjustment logic only -- each drug's own
    clearance equation (Module 4) uses continuous CrCl directly, not this category.
    """
    if crcl_ml_min >= 90:
        category = "Normal"
    elif crcl_ml_min >= 60:
        category = "Mild"
    elif crcl_ml_min >= 30:
        category = "Moderate"
    else:
        category = "Severe"
    return {
        "category": category, "crcl_ml_min": crcl_ml_min,
        "reference": "FDA Guidance for Industry, Pharmacokinetics in Patients with "
                      "Impaired Renal Function, Table 1, p.7"
    }
```

## Worked examples
| Case | CrCl | Weight basis | Category |
|---|---|---|---|
| 65yo male, 70kg, 175cm, SCr 1.0 | 72.9 mL/min | actual (below IBW) | Mild |
| 65yo male, 110kg, 175cm, SCr 1.0 | 89.9 mL/min | adjusted body weight | Mild |

Note the obesity case: using raw actual weight (110kg) would have inflated CrCl well
past what's physiologically plausible for this patient; the adjustment brings it down
to 89.9 mL/min -- just under the Normal/Mild boundary, illustrating why the weight
correction matters for categorical logic, not just the raw number.

## Open item carried forward
Weight-selection thresholds (actual/IBW/30%-adjusted) reflect established general
dosing practice and are now confirmed sourced (Bauer Ch.3 p.56; Winter Ch.3 p.104-105
Eq.3.9), triggered at >30% over IBW.

**Superseding correction (see pk_reference_values.csv, "Weight basis for Vd" row):**
the general Cockcroft-Gault weight-selection rule in this file applies to CrCl itself,
but each drug's own Vd equation (used in Module 4, Stage 8) has its OWN weight basis,
not a single shared rule:
- Gentamicin: V = 0.26 x [IBW + 0.4(TBW-IBW)]; additionally, obese CrCl should use
  the **Salazar-Corcoran equation instead of Cockcroft-Gault** -- this equation is
  NOT yet sourced and is an open gap before gentamicin dosing in obese patients can
  be considered complete
- Vancomycin: clearance uses TBW (kidney hypertrophy in obesity), but Vd uses IBW
  (Vd = 0.7 L/kg x IBW) -- clearance and Vd use DIFFERENT weight bases for this drug
- Digoxin: Vd uses IBW (V = 7 L/kg x IBW) -- supersedes the 6.0 L/kg x actual-weight
  figure used in Stage 8A's worked example; that example will need re-running once
  `pk_engine.py` is actually built (no committed code yet, so no retroactive fix needed
  today)
- Phenytoin: V = 0.7 L/kg x [IBW + 1.33(TBW-IBW)]

This module's Cockcroft-Gault weight-selection function remains correct for CrCl
itself; it should NOT be assumed to also be the correct weight basis for each drug's
Vd equation in Module 4 -- that is a separate, drug-specific decision, now documented
in `pk_reference_values.csv`.
