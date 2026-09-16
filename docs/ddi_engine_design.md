# DDI Engine Design (Module 3)

## Lookup design
Order-independent pair lookup keyed by `frozenset({drug_a, drug_b})`, so a query for
(A,B) and (B,A) return the same record. Loaded once from `data/ddi_knowledge_base.csv`.

**Important distinction preserved by design:** a pair absent from the knowledge base
returns `pair_found_in_kb: False` with an explicit note that this does NOT mean the
interaction has been ruled out -- it means it falls outside this project's sourced
6-pair set. Only pairs explicitly marked `interaction_present=NO` with a documented
negative search (per `data_sources_policy.md`) represent a checked-and-confirmed
absence. Collapsing these two cases would misrepresent an unchecked pair as a
verified-safe one -- a real safety distinction, not a technicality.

```python
import csv

class DDIEngine:
    """
    Loads the DDI knowledge base and provides order-independent pair lookup.
    Source data: data/ddi_knowledge_base.csv (see docs/data_sources_policy.md).
    """
    def __init__(self, csv_path: str):
        self._lookup = {}
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = self._make_key(row["drug_a"], row["drug_b"])
                if key in self._lookup:
                    raise ValueError(
                        f"Duplicate DDI pair found: {row['drug_a']} + {row['drug_b']}"
                    )
                self._lookup[key] = row

    @staticmethod
    def _make_key(drug_a: str, drug_b: str) -> frozenset:
        return frozenset({drug_a.strip().lower(), drug_b.strip().lower()})

    def check_pair(self, drug_a: str, drug_b: str) -> dict:
        key = self._make_key(drug_a, drug_b)
        record = self._lookup.get(key)
        if record is None:
            return {
                "pair_found_in_kb": False,
                "drug_a": drug_a, "drug_b": drug_b,
                "note": "Pair not present in knowledge base. This does NOT mean "
                        "an interaction has been ruled out -- it means no "
                        "interaction was documented in this project's sourced "
                        "6-pair set. Only pairs marked interaction_present=NO "
                        "with a documented negative search represent a checked "
                        "absence."
            }
        return {"pair_found_in_kb": True, **record}

    def check_all_pairs(self, drug_list: list[str]) -> list[dict]:
        results = []
        for i in range(len(drug_list)):
            for j in range(i + 1, len(drug_list)):
                results.append(self.check_pair(drug_list[i], drug_list[j]))
        return results
```

## Patient-adjusted severity — sourcing decision (locked)

`module_design.md` calls for Module 3 to output both literature severity and a
patient-adjusted severity. For the Vancomycin+Gentamicin pair specifically (the only
pair in the current knowledge base where renal-status escalation would plausibly
apply):

**What was checked:**
- Rybak 2020 (already cited) and vancomycin-AKI risk-factor literature list concomitant
  nephrotoxic agents as a risk factor, alongside trough/AUC level and treatment duration
- A 2023 multicentre study (*J Antimicrob Chemother*) found baseline renal dysfunction
  was NOT shown to be an independent, graded risk factor for vancomycin-associated AKI
  -- it functions more as a general illness-severity marker than a step-wise multiplier
- No source reviewed defines a quantitative or tiered escalation rule (e.g., "severity
  moves from High to Critical below CrCl X") for this pair specifically

**Decision: keep severity adjustment qualitative in v1.** No authoritative source
provides a sourced, renal-status-dependent escalation rule for this pair. The existing
literature severity (High) and its recommendation (frequent renal monitoring,
mandatory TDM, consider extended-interval gentamicin dosing) already reflect what the
literature actually supports -- increased monitoring intensity, not a formally graded
severity score keyed to CrCl bands. No numeric escalation rule will be fabricated.
Revisit only if a future source explicitly defines one.

**Implementation consequence:** Module 3's "patient-adjusted severity" field, for this
pair, is populated with the same literature severity plus a renal-status-aware
monitoring note (e.g., "renal impairment present -- monitoring recommendations above
apply with increased urgency"), rather than a separately computed/escalated severity
tier. This should be stated explicitly in the eventual Methods section as a deliberate
scope limitation, not silently implemented as if a graded rule existed.
