# Final Project Audit

## Clinical correctness
- STATUS: Mostly strong. Every equation sourced to a specific page/paper
  (`key_equation_sources.md`, `pk_reference_values.csv`)
- OPEN GAP: gentamicin's Salazar-Corcoran equation for obese-patient CrCl not
  yet sourced (Stage 10)
- OPEN GAP: drug-specific IBW/adjusted-weight Vd corrections (gentamicin,
  vancomycin, phenytoin) not yet implemented in `pk_engine.py` — code still uses
  actual weight (Stage 18 flag)

## Mathematical correctness
- STATUS: Strong, with real bugs caught and documented rather than hidden — the
  vancomycin mL/min->L/hr conversion error (Stage 8A) is preserved as a regression
  test (`test_vancomycin_unit_conversion_regression`), and the digoxin Vd correction
  (6.0 -> 7.0 L/kg) is documented in the watchlist as resolved

## Data quality
- STATUS: Strong. Every DDI/PK fact has a reference field; no fabricated data
  anywhere (`data_sources_policy.md`)
- OPEN: `validation_cases.csv` still has zero real rows (Stage 21, ongoing)

## ML correctness
- STATUS: Honestly scoped rather than "correct" in a generalization sense —
  deliberately not claiming predictive validity given n=6 with a singleton class
  (Stage 11/12)

## Validation
- STATUS: INCOMPLETE. This is the project's single biggest open item. Framework
  and comparison code are ready (`validation_framework.md`, `src/validation.py`);
  real cases are not yet collected

## Explainability
- STATUS: Strong. SHAP scoped honestly (Stage 13), equation-trace pattern applied
  consistently across all deterministic modules (Stage 7)

## Software quality
- STATUS: Good for project scope. Type hints, docstrings with sources, explicit
  ValueError over silent failures, tests mirror src/ structure (Stage 16-17)

## Security/privacy
- STATUS: Not formally audited — no real patient data is used anywhere in this
  project (all data is either literature-derived or explicitly-flagged synthetic),
  which substantially limits privacy risk by design rather than by added controls

## Documentation
- STATUS: Strong — 29 stages, each with a saved decision record and rationale,
  not just a final summary

## Reproducibility
- STATUS: Good — README, requirements.txt, model card, fixed random seeds
  (Stage 28)

## Research quality
- STATUS: Honest and appropriately scoped — novelty claim calibrated to what
  the project actually supports (Stage 22), statistical methods matched to
  sample size (Stage 24), no fabricated results anywhere

## Publication readiness
- STATUS: NOT YET READY. Blocked specifically on Stage 21 (real validation cases).
  Once validation cases exist: Abstract, Results 6.1, and Discussion sections of
  `manuscript_outline.md` can be completed, and the project would be genuinely
  submission-ready for a scoped feasibility-study framing (per `paper_titles.md`)

## Priority checklist before considering this "done"
1. [ ] Collect and run real validation cases (Stage 21) — blocks Abstract/Results
2. [ ] Source Salazar-Corcoran equation for obese gentamicin dosing (Stage 10 gap)
3. [ ] Implement drug-specific Vd weight corrections in pk_engine.py (Stage 18 gap)
4. [ ] Draft Abstract and Results once #1 is resolved
5. [ ] Full read-through against every "Limitations" item to confirm nothing is
   glossed over in the actual manuscript text
