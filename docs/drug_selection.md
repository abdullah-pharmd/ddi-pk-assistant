

Drug selection · MD
Drug Selection — DDI + PK Dosing Assistant
Decision
Keep all four drugs from coursework: Vancomycin, Gentamicin, Phenytoin, Digoxin.

Phenytoin is included as an explicit architectural special case (Michaelis-Menten / nonlinear kinetics), not forced into the same equation framework as the other three.

Why each drug is included
Vancomycin — renally-scaled dosing, core TDM drug, in-set DDI partner with gentamicin (shared nephrotoxicity/ototoxicity concern). Note: dosing guidance has moved from trough-based toward AUC-guided monitoring in recent practice — we will explicitly decide and document which approach the tool models (Stage 8) rather than picking one silently.
Gentamicin — renally-scaled dosing, narrow therapeutic index, classic peak/trough TDM, in-set DDI partner with vancomycin.
Digoxin — renally-scaled dosing, narrow therapeutic index, P-glycoprotein-mediated DDI mechanism (adds mechanistic breadth beyond CYP), classic TDM drug.
Phenytoin — nonlinear (Michaelis-Menten) elimination kinetics, unlike the other three's first-order kinetics. Extensive CYP-mediated DDIs. Included because it is the harder case, not despite it — modeling it correctly (rather than approximating it as linear, which would be clinically wrong) is a genuine methodological contribution.
Architecture implication for Module 4 (Pharmacokinetic Engine)
Module 4 will be built with two distinct paths:

Linear / first-order path — shared framework for vancomycin, gentamicin, digoxin
Nonlinear / Michaelis-Menten path — dedicated to phenytoin
These are NOT to be merged into one equation. Each path gets its own derivation, assumptions, and validation cases (Stage 8, Stage 21).

Consequences accepted
Stage 8 requires a dedicated phenytoin subsection with its own equation derivation
Stage 21's literature validation set needs phenytoin-specific reference cases, separate from the linear-kinetics drugs
Vancomycin's dosing model (trough vs. AUC-guided) must be explicitly stated and sourced before Stage 8 is considered complete
