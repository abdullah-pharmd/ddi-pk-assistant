# Validation Against Literature — Framework

## Status
`data/validation_cases.csv` currently has the header schema only (Stage 8). This
document defines the methodology; real cases must come from actual textbook/paper
worked examples, per the project's data-honesty requirements (project_scope.md).

## Metrics, matched to case type
- **PK numeric results** (concentration, half-life, dose): percent error
  `(calculated - reported) / reported x 100%`
- **DDI severity / renal category**: match/mismatch, reported as "X of N pairs
  matched" — NOT a percentage, given the small expected case count (avoids
  overstating precision, consistent with Stage 11/12's small-dataset honesty)
- Explicitly NOT computed: sensitivity/specificity, ROC-type metrics — these need
  far more cases than this project will realistically have

## Priority cases (targets known open items, not collected at random)
| Priority | Case needed | Resolves |
|---|---|---|
| High | Published vancomycin case (age/weight/CrCl -> reported CL or t half) | Stage 8A's 10.17 hr edge-case flag |
| High | Published digoxin case with NYHA class stated | Confirms the corrected Vd=7 L/kg fix from Stage 18 |
| Medium | Gentamicin case | Cross-check even though currently unflagged |
| Medium | Phenytoin case with low albumin | Tests Vmax/Km equation + Winter-Tozer correction together |
| Lower but valuable | Case with 2+ of the 4 drugs together | Validates DDI severity against a real documented outcome |

## What a usable case needs
- Patient parameters exactly as reported (age, weight, CrCl or inputs to derive it,
  any drug-specific input like NYHA class or albumin)
- The reported result (concentration, dose, half-life — whatever the source gives)
- Full citation (same standard as `data_sources_policy.md`)

## Process once cases arrive
1. Enter into `data/validation_cases.csv`
2. Run the same parameters through the tool's actual functions
3. Compare with `src/validation.py`'s `numerical_error()` or `categorical_agreement()`
4. Aggregate with `summarize_validation_run()`
5. Results table (case ID, drug, reported, calculated, % error, source) becomes the
   Results section's validation table (Stage 26)

## Deliverable this produces for the manuscript
One results table: case ID, drug, reported value, calculated value, % error, source.
No figures generated until real numbers exist to plot.
