# Data Sources Policy — DDI + PK Dosing Assistant

## Purpose
This policy governs where every clinical fact, equation, threshold, or guideline used in
this project must come from. It formalizes the sourcing standard already applied in
`ddi_knowledge_base.csv` and `pk_reference_values.csv`, so it stays consistent for
everything still to be built (Stage 9 renal module, Stage 10 DDI engine, Stage 21
validation cases).

## Source-type mapping

| Information type | Preferred source(s) | Why |
|---|---|---|
| Drug interaction facts (mechanism, severity, effect) | Peer-reviewed literature (PMID-verifiable), FDA/DailyMed labeling | Primary literature allows a specific, checkable citation per fact |
| PK equations/parameters | Established clinical pharmacokinetics textbooks (e.g., Bauer, Winter, Shargel & Yu) | Textbooks aggregate and validate equations; citing a specific page is standard practice for well-established equations |
| Dosing guidelines / therapeutic ranges | Specialty-society consensus guidelines (e.g., ASHP/IDSA/PIDS/SIDP 2020) over textbook defaults, when a specific current guideline exists | Guidelines get revised over time; always prefer the current guideline over an older textbook default when they conflict |
| Renal/hepatic dose adjustment rules | FDA/DailyMed labeling + nephrology/hepatology-specific literature where the label is silent | Labels are the regulatory baseline; specialty literature fills genuine gaps |
| TDM interpretation thresholds | The specific study/trial that established the threshold (e.g., DIG trial post-hoc for digoxin) | A threshold should trace to the study that established it, not "common knowledge" |
| Negative findings ("no interaction found") | Documented negative search — state the database/checker and search terms | A negative claim still needs to say how the search was conducted |

## Explicitly NOT acceptable as a source
- General web pages, drug-info apps, or forums without a citable underlying primary/secondary source
- The project author's own clinical reasoning presented as a sourced fact (reasoning is
  appropriate for *design decisions* — e.g., choosing AUC-guided vancomycin dosing over
  trough-only — but the underlying clinical fact still needs its own citation)
- AI-generated content, including content generated in this project's development
  process, treated as a source in itself — AI assistance may help structure or reason
  about sources but cannot verify or originate one

## Standing practice going forward
- Every clinical fact gets a reference field, no exceptions (including negative findings)
- When guideline and textbook conflict, state both, pick the current guideline as primary,
  and document the older one as legacy — do not silently choose one or present both as
  equally valid (per the digoxin range and vancomycin dosing model decisions in
  `data_strategy.md`)
- Equation-level citations should be pinpoint (chapter/page or article) wherever possible,
  not a general reference line
- All cited sources should be spot-checked by the author (or an advisor) before inclusion
  in any manuscript or competition submission