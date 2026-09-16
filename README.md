# ddi-pk-assistant

A clinical decision support prototype connecting renal function estimation, classical pharmacokinetics, and drug-drug interaction surveillance.

### Problem
Hospital order-entry systems fire interaction warnings indiscriminately. Studies in tertiary hospitals (van der Sijs et al., 2006; Weingart et al., 2003) show that prescribers override 73% to 96% of these warnings. Most overrides happen because the software checks drug names in pairs without reading the patient's lab results or considering renal elimination.

At the same time, precision dosing tools (Keizer et al., 2020; Gillaizeau et al., 2013) calculate pharmacokinetic doses for single medications in isolation, ignoring concurrent interacting drugs.

This repository prototypes a workflow that runs both assessments together:
1. Calculates patient-specific creatinine clearance using Cockcroft-Gault with weight adjustments (ideal body weight and adjusted body weight for obesity).
2. Computes pharmacokinetic parameters for four narrow-therapeutic-index drugs (gentamicin, vancomycin, digoxin, phenytoin) using classical deterministic models from Larry Bauer's *Applied Clinical Pharmacokinetics*.
3. Evaluates drug pairs against a curated interaction table, separating true pharmacokinetic interactions from assay artifacts (such as the vancomycin-digoxin PETINIA immunoassay cross-reaction).
4. Flags dose-adjustment needs when renal impairment or severe interactions coexist.

### Implemented models

#### Renal clearance
- Equation: Cockcroft-Gault (1976)
- Weight protocols: Devine ideal body weight (IBW), and adjusted body weight (0.4 factor) for patients exceeding 120% of IBW.
- Renal staging: FDA guidance thresholds (normal >=90, mild 60-89, moderate 30-59, severe 15-29, end-stage renal disease <15 mL/min).

#### Pharmacokinetics
- Gentamicin: Single-compartment intravenous infusion model. Elimination rate ke = 0.00293 * CrCl + 0.014 hr^-1, Vd = 0.26 L/kg.
- Vancomycin: Matzke clearance model adapted to patient weight. Clearance = 0.695 * CrCl + 0.05 * weight (kg). Vd = 0.7 L/kg (uses IBW if patient exceeds 130% of IBW). Daily dose targets an AUC24 of 500 mg*hr/L.
- Digoxin: Jusko-Koup model. Total clearance = 1.303 * CrCl + nonrenal clearance, where nonrenal clearance depends on heart failure severity (NYHA class I-IV).
- Phenytoin: Capacity-limited Michaelis-Menten kinetics (Richens and Dunlop, 1975) with Vmax = 7 mg/kg/day and Km = 4 mg/L. Includes Winter-Tozer albumin correction for hypoalbuminemia.

#### Drug interaction knowledge base
A focused reference table covering narrow-therapeutic-index drugs. Each pair includes mechanism, clinical effect, severity tier, actionable recommendation, and primary literature citation. Notably, vancomycin plus digoxin is documented as an analytical cross-reactivity artifact on PETINIA assays rather than in vivo toxicity.

### Project layout
```
ddi-pk-assistant/
|-- app.py                     # Streamlit web interface
|-- requirements.txt           # Python dependencies
|-- src/
|   |-- renal.py               # Cockcroft-Gault and body weight calculations
|   |-- pk_engine.py           # Pharmacokinetic equations for all 4 drugs
|   |-- ddi_engine.py          # Pairwise interaction lookup
|   |-- dose_adjustment.py     # Decision logic combining renal and DDI outputs
|   |-- tdm.py                 # Reference ranges and concentration checks
|   |-- batch_processing.py    # Multi-patient CSV handling
|   |-- report_generator.py    # PDF report generation
|   `-- validation.py          # Input ranges and clinical sanity checks
|-- data/
|   |-- ddi_knowledge_base.csv # Sourced interaction pairs
|   `-- sample_batch.csv       # Test cohort for batch screening
|-- tests/
|   |-- test_renal.py          # Cockcroft-Gault edge cases and weight logic
|   |-- test_pk_engine.py      # Numerical checks against textbook worked cases
|   `-- test_ddi_engine.py     # Interaction queries and bidirectional lookup
`-- docs/                      # Clinical background and design notes
```

### Verification and tests
All formulas are tested against worked clinical cases in Bauer's *Applied Clinical Pharmacokinetics* (2nd edition, McGraw-Hill, 2008). 

Run the test suite:
```bash
pytest tests/ -v
```
All 26 unit tests run deterministically in under half a second.

### Running the application locally

1. Clone this repository:
```bash
git clone https://github.com/abdullah-pharmd/ddi-pk-assistant.git
cd ddi-pk-assistant
```

2. Set up a virtual environment:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux or macOS:
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start Streamlit:
```bash
streamlit run app.py
```

The application runs two modes:
- Single patient: Enter demographics, renal laboratory values, and medications to inspect step-by-step calculations and download a PDF summary.
- Batch processing: Upload a multi-row CSV to screen hospital ward lists for renal dose adjustments and interactions simultaneously.

### Clinical disclaimer
This repository is an academic research prototype. It is not approved as a medical device and should never be used as the sole basis for clinical treatment, diagnosis, or prescribing. All calculations and recommendations must be reviewed by licensed clinical pharmacists and attending physicians under institutional hospital protocols.


