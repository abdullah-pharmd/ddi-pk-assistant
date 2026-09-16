# Clinical Module Design — DDI + PK Dosing Assistant

## Module 1 — Patient & Medication Input
- **Answers:** data contract for all other modules
- **Inputs:** age, sex, weight, height, serum creatinine, indication, drug(s) + current
  dose/frequency/route, measured concentration (optional — only if a TDM sample exists),
  hepatic impairment flag (yes/no/unknown — flag only, not calculated, per scope)
- **Conditional input (digoxin only):** NYHA heart-failure class (I–IV) — REQUIRED when
  digoxin is one of the patient's drugs, since it directly determines ClNR (nonrenal
  clearance) in Module 4's digoxin equation (40 mL/min for NYHA I–II, 20 mL/min for
  NYHA III–IV; see `pk_reference_values.csv`). Not required for the other three drugs —
  this is drug-specific conditional input, not a universal field.
- **Outputs:** one validated, structured patient record
- **Note:** no open-ended "other lab values" field — any additional lab value needed by a
  specific drug (e.g. albumin for phenytoin protein-binding correction) is named explicitly
  when that drug's PK logic is built (Stage 8), not bundled here as a catch-all

## Module 2 — Renal Function
- **Answers:** precursor to the dose-adjustment question
- **Inputs:** age, sex, weight, serum creatinine (Module 1)
- **Outputs:** CrCl (Cockcroft-Gault, raw/unnormalized mL/min), renal category
  (thresholds sourced in Stage 9)
- **Feeds:** Module 4 (PK engine) and Module 3 (DDI — renal status can change clinical
  significance, e.g. nephrotoxic combinations)
- **Note:** outputs raw CrCl only — this is why digoxin's PK engine (Module 4) uses the
  Jusko-Koup method rather than the Jelliffe/BSA-normalized method, to stay consistent
  with this module's output rather than requiring a second, inconsistent CrCl calculation

## Module 3 — DDI Assessment
- **Answers:** interaction presence, mechanism, severity, monitoring, ML risk classification
- **Inputs:** drug list (Module 1), renal category (Module 2)
- **Outputs:** per drug pair — interaction (y/n), mechanism (PK/PD), pathway if known,
  literature severity, patient-adjusted severity (kept as a SEPARATE field, not merged),
  monitoring recommendation, source, ML risk classification + SHAP explanation for flagged pairs

## Module 4 — Pharmacokinetic Engine
- **Answers:** clearance, half-life, loading/maintenance dose, dosing interval
- **Inputs:** drug identity, patient weight/age, CrCl (Module 2), NYHA class (Module 1,
  digoxin only)
- **Outputs:** clearance, half-life, loading dose (drug-dependent — not all drugs use one),
  maintenance dose, dosing interval — each tagged with equation used + reference
- **Architecture:** two paths — linear/first-order (vancomycin, gentamicin, digoxin,
  each with drug-specific equations and unit-conversion steps) and nonlinear/
  Michaelis-Menten (phenytoin only) — see `drug_selection.md`

## Module 5 — Dose Adjustment (integration point)
- **Answers:** does the calculated dose need adjusting, and why
- **Inputs:** calculated dose (Module 4), renal category (Module 2), hepatic flag (Module 1),
  DDI findings (Module 3), TDM interpretation (Module 6)
- **Outputs:** adjusted dose recommendation if criteria are met, with reason(s) cited
  (renal / hepatic flag / interacting drug / out-of-range concentration, or a combination);
  hepatic output capped at a caution flag only, never a calculated new dose
- **This is the only module reading from all four upstream modules** — it is where the
  project's core integration (Stage 1's "actual novelty") happens

## Module 6 — TDM Interpretation
- **Answers:** is the current/estimated concentration within therapeutic range
- **Inputs:** measured concentration if provided, else estimated concentration (Module 4),
  drug-specific therapeutic range
- **Outputs:** below/within/above range, qualitative direction of adjustment (a human
  decides the actual new number — this module does not auto-recalculate a dose)
- **Feeds:** Module 5 — an out-of-range level is itself grounds to hold/adjust a dose,
  independent of renal status or a DDI
- **Note:** drug-gated — only runs for drugs where TDM is clinically standard (all four in
  this project qualify)

## Module 7 — Explainability
- **Answers:** why was this DDI classified this way (ML); why was this number calculated
  this way (deterministic modules)
- **Inputs:** Module 3's ML output (for SHAP), Modules 4–6's calculations (for an equation
  trace — inputs plugged into a formula, not a model explanation)
- **Outputs:** two structurally separate explanation types, so a user never mistakes a
  deterministic calculation trace for a model explanation

## Data flow

```
Module 1 (Patient Input, incl. NYHA if digoxin)
        |
        v
Module 2 (Renal Function) ------------------+
        |                                   |
        v                                   v
Module 4 (PK Engine) <--- NYHA (digoxin)   Module 3 (DDI Assessment) --> Module 7 (SHAP)
        |                                   |
        v                                   |
Module 6 (TDM Interpretation)                |
        |                                   |
        +--------> Module 5 (Dose Adjustment) <--------+
                          |
                          v
                  Module 7 (Equation trace)
```

Module 5 reads from Modules 2, 3, 6, and Module 1's hepatic flag — the only module in the
system that converges all four. This is the concrete implementation of Stage 2's Question 8
(renal integration) and its extension to include TDM-driven adjustment.

## Revision log
- Stage 8A (digoxin equation review): added NYHA heart-failure class as a required
  conditional input to Module 1, specific to digoxin. Discovered while sourcing the
  digoxin ClNR value, which is heart-failure-severity dependent, not a fixed constant.