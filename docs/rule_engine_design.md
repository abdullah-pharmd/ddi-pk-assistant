# Clinical Rule Engine Design — DDI + PK Dosing Assistant

## Core principle
Deterministic clinical calculations must never be replaced by ML approximations.
ML is used only where no closed-form equation exists in the literature.

## The boundary (locked)
- **Deterministic (formula-based), no ML:**
  - Module 2 — Renal Function (Cockcroft-Gault)
  - Module 4 — Pharmacokinetic Engine (clearance, Vd, half-life, loading/maintenance
    dose, dosing interval — including phenytoin's Michaelis-Menten path)
  - Module 5 — Dose Adjustment (rule-based combination of renal/hepatic/DDI/TDM inputs)
  - Module 6 — TDM Interpretation (range comparison against sourced therapeutic ranges)
- **ML-based:**
  - Module 3 — DDI risk classification only. This is the one component where the
    target relationship (interaction severity/urgency, synthesized from mechanism +
    patient factors) is not a published closed-form equation anywhere in the
    literature, and is exactly the kind of relationship ML is suited to model.

## Why the deterministic components stay deterministic
- The underlying relationships (Cockcroft-Gault, clearance equations, Michaelis-Menten
  kinetics) are known, published, closed-form — training a model to approximate them
  would introduce unnecessary error into a calculation that should be exact
- Deterministic output is auditable by hand; model output is a probability estimate,
  not a guaranteed-correct calculation
- ML earns its place only where the relationship is genuinely unknown/too complex to
  specify by hand — not merely because ML is available

## The rule-engine pattern
Every deterministic module output follows the same five-step shape:

```
Input -> Clinical Rule/Equation -> Calculation -> Result -> Explanation -> Reference
```

Example (Cockcroft-Gault):
```
Input: age, weight, sex, serum creatinine
Rule: Cockcroft-Gault equation (cited)
Calculation: CrCl = [(140-age) x weight x (0.85 if female)] / (72 x SCr)
Result: CrCl value + renal category
Explanation: plain-language statement of which equation and which inputs were used
Reference: pinpoint citation
```

This shape is what Module 7's "equation trace" explanation surfaces directly — it does
not need to generate novel explanations, only expose these five fields per calculation.