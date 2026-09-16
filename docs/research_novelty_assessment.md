# Research Novelty Assessment

## Candidates evaluated

| Candidate | Novel? | Assessment |
|---|---|---|
| Standalone DDI checker | No | Widely available (Drugs.com, Lexicomp, Epocrates, etc.) |
| Standalone PK dosing calculator | No | Widely available in clinical pharmacy tools |
| SHAP-on-a-classifier alone | Weak alone | Now a standard technique, not novel by itself |
| **Cross-domain integration: renal status simultaneously informs dose calculation AND DDI severity interpretation, in one patient-specific pipeline** | **Yes** | Most public DDI checkers do not take renal function as an input; most PK calculators do not cross-reference concurrent DDIs. Module 5's convergence of Modules 2, 3, and 6 is a genuine architectural contribution |
| **Honest, data-size-appropriate ML framing** (Stage 11-12: refusing misleading cross-validation on a singleton class, refusing unsourced synthetic augmentation) | Yes, modestly | A deliberate methodological point, not just a limitation to apologize for |
| **Explicit rule-engine/ML boundary with stated justification** (Stage 7) | Yes, modestly | Many comparable student projects apply ML indiscriminately; this project's justification for keeping PK/renal deterministic is a citable design decision |
| Full sourcing traceability (every clinical fact cited to a specific page/paper) | Not novelty per se, but a genuine strength | Differentiates this prototype's credibility from typical student projects |

## Verdict
The project has one genuine, defensible novelty claim: **the patient-specific
cross-domain integration (renal status simultaneously informing dose calculation and
DDI interpretation), combined with a deliberately transparent, honestly-scoped
hybrid rule+ML architecture.**

This is real but modest. Appropriate framing for the paper: "a methodologically
rigorous, integrated decision-support prototype demonstrating [cross-domain
integration + honest small-data ML design]" — NOT "a novel AI system for predicting
drug interactions." Overclaiming here is the most likely way to undermine an
otherwise defensible project in front of a reviewer.

## What would strengthen the claim further
- Completing Stage 21 with real validation cases
- Expanding the DDI knowledge base (Stage 11's Future Work path) toward a genuine
  predictive claim
- Explicit limitations in the paper — the honest scope is itself part of what makes
  the novelty claim credible rather than inflated
