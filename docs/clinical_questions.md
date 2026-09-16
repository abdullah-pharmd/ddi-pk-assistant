

Clinical questions · MD
Clinical / Research Questions — DDI + PK Dosing Assistant
DDI questions
Is there a known interaction between the patient's drugs?
What is the mechanism (PK or PD), and which pathway (e.g., CYP, P-gp) if known?
What is the clinical severity/significance?
What is the recommended monitoring or action?
PK / dosing questions
What is the patient's estimated clearance and half-life for this drug?
What loading dose (if applicable to this drug) and maintenance dose are indicated?
What dosing interval is appropriate?
Renal integration question
Does the patient's renal function require adjusting the dose calculated in Q6/Q7?
TDM question
Is the patient's current/estimated concentration within, below, or above the therapeutic range, and does that suggest a dose change?
Explainability question (ML-scoped only — applies to DDI risk classification, not
the deterministic PK/renal calculations)
Which patient/drug factors drove the DDI risk classification?
Hepatic question (flag-only, per project_scope.md)
Is hepatic impairment clinically relevant for this drug, and does it warrant a caution flag (not a calculated adjustment)?
Notes
Loading dose (Q6) is drug-dependent, not universal — gentamicin/vancomycin routinely use one, digoxin sometimes, phenytoin situationally. Handled per-drug in the PK engine (Stage 8), not as a forced universal output.
Q8 is the explicit statement of the cross-domain integration that distinguishes this project's scope (Option D) from a simple DDI+PK bolt-together (Option C).

