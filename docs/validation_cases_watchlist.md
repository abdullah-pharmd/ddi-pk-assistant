# Validation Cases Watchlist (informal — Stage 21 will formalize into validation_cases.csv)

This is a running note of calculated results that fell at the edge of the reference
range and should be checked against a real literature/textbook worked example once
Stage 21 (Validation Against Literature) begins. Not yet real validation data —
these are flags for follow-up, not confirmed cases.

## 1. Vancomycin — edge case
- **Patient:** 70 kg, CrCl 80 mL/min
- **Calculated:** CL = 55.65 mL/min = 3.34 L/hr, t½ = 10.2 hr
- **Reference file range:** normal renal function t½ = 4–6 hr
- **Flag:** calculated t½ is noticeably above the stated normal range for this patient.
  Possibly explained by CrCl 80 being only moderately good (not fully "normal") and a
  population-average Vd (0.7 L/kg) not fitting this specific patient — but needs
  checking against a real worked example, not assumed correct.

## 2. Digoxin — edge case (RESOLVED at Stage 18 code implementation)
- **Patient:** 70 kg, CrCl 80 mL/min, NYHA I–II (no/mild heart failure)
- **Original calculated (Stage 8A, using placeholder Vd=6.0 L/kg x actual weight):**
  CL = 144.24 mL/min = 8.654 L/hr, Vd = 420 L, t½ = 33.6 hr
- **Corrected (Stage 18, using sourced Vd=7.0 L/kg per pk_reference_values.csv):**
  Vd = 490 L, t½ = 39.2 hr (NYHA I-II) / 45.6 hr (NYHA III-IV)
- **Reference file range:** normal renal function t½ = 36–48 hr
- **Resolution:** both corrected values now land comfortably inside the reference
  range, unlike the original placeholder-based calculation. Still worth a literature
  cross-check at Stage 21, but no longer flagged as an anomaly needing investigation.

## Not yet flagged
- Gentamicin: worked example (t½ = 2.79 hr) landed inside the stated 2–3 hr range —
  no flag needed, but still worth a literature cross-check at Stage 21 like the others.
- Phenytoin: not yet built (Stage 8B, pending).
