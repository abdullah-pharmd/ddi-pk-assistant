# Stage 21 — Validation Against Literature (COMPLETE)

## Cases used
4 real, cited worked examples from Bauer LA, *Applied Clinical Pharmacokinetics*,
2nd ed. — Vancomycin Examples 1-2 (Ch.5, pp.218-221), Digoxin Examples 1&3 (Ch.6,
pp.314-316). Full detail in `data/validation_cases.csv`.

One case (Digoxin Example 4, obese patient) was deliberately EXCLUDED after the
reported V could not be reconciled against the source formula using either IBW or
TBW as the weight term — flagged for future re-verification rather than used with
an unreconciled reference value. This exclusion is itself worth citing in the
paper as evidence of validation rigor.

## Results

| Case | Drug | Metric | Reported | Calculated | % Error |
|---|---|---|---|---|---|
| V1 | Vancomycin | t1/2 (hr) | 8.0 | 7.98 | -0.2% |
| V2 | Vancomycin | t1/2 (hr) | 27.0 | 27.11 | +0.4% |
| D1 | Digoxin | maintenance dose (ug/day) | 288 | 287.5 | -0.2% |
| D2 | Digoxin | maintenance dose (ug/day) | 87 | 86.5 | -0.6% |

**Mean absolute % error: 0.3%. Max absolute % error: 0.6%.**

## Real bug caught and fixed during this stage
Validation against Case V2 initially showed a 20.3% error (V1 showed 4.9%) --
large enough to investigate rather than dismiss as rounding. Root cause: Bauer's
own worked examples apply vancomycin's nonrenal clearance constant on a
mL/min/kg basis (`0.05 * weight_kg`), not as a flat `+0.05 mL/min` regardless of
patient size, as the original Stage 8A implementation assumed. This is the same
category of scaling/unit error as the mL/min-to-L/hr bug caught earlier in Stage
8A -- caught here specifically BECAUSE real validation data existed to catch it
against. Fixed in `src/pk_engine.py`, locked in as a named regression test
(`test_vancomycin_nonrenal_constant_scales_with_weight`), and documented in
`pk_reference_values.csv`.

## What this demonstrates for the paper
- The deterministic PK engine reproduces literature-reported values to within
  <1% average error across both drugs tested, for both normal and impaired renal
  function scenarios
- The validation process itself caught a real implementation error that
  worked-through-once code review had missed -- this is a genuine methodological
  point: validation against independent reference cases is what surfaced this,
  not code review alone
- Gentamicin and phenytoin remain unvalidated against literature cases (no cases
  collected yet) -- stated as a limitation, not implied as validated
