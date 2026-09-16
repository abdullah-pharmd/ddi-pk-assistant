# Coding Strategy

## Language & libraries (updated from original Part 4 — XGBoost dropped per Stage 11)
```
Python 3.10+
pandas, numpy       -- data handling
scikit-learn        -- Random Forest (Module 3 ML side)
shap                -- Module 7 ML explainability
streamlit           -- UI
matplotlib          -- SHAP plot rendering
pytest              -- testing
fpdf2 or reportlab  -- PDF export (decided at Stage 20)
```

## Function convention (locked — formalizes the pattern used throughout Stages 8-10)
```python
def some_calculation(patient_param: float, ...) -> dict:
    """
    One-line summary of what this calculates.
    Source: [pinpoint citation, matching pk_reference_values.csv / ddi_knowledge_base.csv]
    NOT valid for: [explicit invalidity conditions]
    """
    return {
        "result_field": value,
        "reference": "citation string",
    }
```

Rules:
- Every function implementing a sourced clinical equation returns a dict with a
  `reference` key -- never a bare number. This is what makes Module 7's equation-trace
  explanation possible without extra plumbing.
- Every docstring states its source and its invalidity conditions.
- Gaps get `raise NotImplementedError` with a specific message -- never a silent
  placeholder number (as practiced for digoxin's ClNR and phenytoin's Vmax/Km before
  those sources arrived).

## Error handling & validation
- Type hints on every function signature
- Explicit ValueError for clinically invalid inputs (negative age, zero weight,
  SCr <= 0)
- No bare `except:` blocks
- Patient input validation (Module 1) happens once at the entry point; downstream
  modules trust the data they receive

## Style
- Functions over one large script; one function per clinical calculation, mapping to
  module_design.md's module breakdown
- No premature class hierarchies -- DDIEngine is a class because it holds loaded state
  (the CSV); PK/renal/TDM functions stay plain functions
- Docstrings for anything a reader needs to trust the output (source, units,
  assumptions); inline comments reserved for non-obvious implementation details (e.g.
  the mL/min -> L/hr conversion catch from Stage 8A)

## Reproducibility
- requirements.txt pins versions once the environment is finalized
- Fixed random_state anywhere randomness appears (Random Forest), so results are
  reproducible run to run -- required given Stage 12's "descriptive fit" framing, which
  would be undermined by a result that changes between runs
