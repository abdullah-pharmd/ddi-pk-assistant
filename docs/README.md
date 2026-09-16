# DDI + PK Dosing Assistant

Educational/research decision-support prototype integrating pharmacokinetic dosing,
renal-function-based dose adjustment, and drug-drug interaction risk assessment for
four drugs: gentamicin, vancomycin, phenytoin, digoxin.

**This is NOT a clinical tool.** All outputs require verification by a qualified
healthcare professional before any clinical use. See `docs/project_scope.md` for
full scope and `docs/research_study_design.md` for limitations.

## Setup
```
pip install -r requirements.txt
streamlit run app.py
```

## Project structure
```
ddi_pk_assistant/
├── app.py              # Streamlit UI (single-patient + batch tabs)
├── src/                # Core modules — see docs/module_design.md
├── data/                # Sourced knowledge base + PK reference values
├── docs/                # Full design documentation and citations (29 stages)
└── tests/               # Unit tests (see docs/testing_strategy.md)
```

## Data sources
Every clinical fact, equation, and threshold in this project is cited to a specific
source. See `docs/data_sources_policy.md` for the sourcing standard and
`data/pk_reference_values.csv` / `data/ddi_knowledge_base.csv` for per-fact citations.

## Model card (ML component)
See `docs/ml_component_design.md`. Summary: Random Forest classifier trained on a
6-row, fully-sourced DDI knowledge base. This is an explainability/audit tool, NOT a
validated predictor — no train/test split or cross-validation performance claim is
made, per documented reasoning in that file.

## Limitations
See `docs/research_study_design.md`, Limitations section, for the complete list —
including known implementation gaps (drug-specific obesity-adjusted Vd corrections
not yet coded) and scope boundaries (4 drugs, 6 DDI pairs, hepatic flag-only).

## Reproducibility
- `requirements.txt` lists exact dependencies
- Fixed random seeds used wherever randomness appears (Random Forest `random_state`)
- Every deterministic calculation traces to a cited equation (see `src/` docstrings)

## Development history
This project was built through a documented 29-stage process, with every clinical
fact sourced before implementation and every code correction (e.g., a unit-conversion
bug caught in Stage 8A) documented rather than silently fixed. Full stage-by-stage
documentation is in `docs/`.
