

Project scope · MD
Project Scope — DDI + PK Dosing Assistant
Decision
Option D, bounded: DDI risk assessment + pharmacokinetic dosing + renal-function-based dose adjustment + TDM interpretation, limited to a small, deliberately selected drug set (finalized in Stage 4).

Why D over the alternatives
Option	Why not chosen
A — DDI only	Not distinctive; DDI checkers are common without a differentiator
B — PK only	A calculator alone isn't a research contribution
C — DDI + PK	Two calculators side by side, not integrated — weaker novelty case
E — Full CDSS	Breadth undermines traceability; every rule needs a verifiable source, which doesn't scale to many drugs for a solo student project
Why D, specifically bounded
The novel contribution is the integration: a patient's renal function feeds into both (a) their calculated dose and (b) how clinically concerning a given DDI is for them specifically. That cross-domain, patient-specific pipeline is the architectural novelty — not drug-count breadth.

Explicitly IN scope for v1
DDI risk assessment (rule-based knowledge base + one ML classification task, SHAP-explained)
Pharmacokinetic dosing calculations (deterministic, formula-based)
Renal-function-based dose adjustment (Cockcroft-Gault-based, drug-specific rules)
TDM interpretation for drugs where it's clinically standard practice
Explicitly OUT of scope for v1
Hepatic dose adjustment beyond basic flagging
Broad, general-purpose DDI coverage (interactions not involving the selected drug set)
Any drug outside the selected set (finalized Stage 4)
Any ML applied to PK/renal calculations — these remain deterministic rules (rationale: Stage 7)
Status
Locked pending Stage 4 (final drug set confirmation).


