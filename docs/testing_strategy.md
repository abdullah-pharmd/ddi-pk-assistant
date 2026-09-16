# Testing Strategy

## Principle
Test cases are drawn from worked examples already produced during Stages 8-10, not
invented separately -- including regression tests against specific bugs caught during
development (e.g., vancomycin's mL/min -> L/hr conversion error from Stage 8A).

## Coverage
- PK engine: normal-case worked examples for all 4 drugs, digoxin NYHA branching,
  phenytoin dose-from-target-Css, phenytoin Winter-Tozer correction (both renal
  scenarios), invalid-input error cases
- Renal module: normal weight, obese/adjusted-weight, category boundary edge values
  (exactly 90, 89.9, 60, 59.9, 30, 29.9)
- DDI engine: known pair lookup, reversed-order equivalence, unknown-pair vs
  confirmed-negative distinction, duplicate-pair-at-load detection
- Edge cases: zero/negative weight, zero/negative SCr (division-by-zero guard),
  negative age, unknown drug names

## Known gap flagged during design
The Stage 9 `crcl_cockcroft_gault` sketch does not yet raise ValueError on zero/
negative inputs -- validation must be added when the real function is written,
per the entry-point validation rule in `coding_strategy.md`.

## Files
```
tests/test_pk_engine.py
tests/test_renal.py
tests/test_ddi_engine.py
```
