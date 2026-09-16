"""
Module 3 (rule-based side) — DDI Engine
Source data: data/ddi_knowledge_base.csv (see docs/data_sources_policy.md).
"""
import csv


class DDIEngine:
    """Loads the DDI knowledge base and provides order-independent pair lookup."""

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
        """
        Returns the literature-level DDI record for a drug pair.
        pair_found_in_kb=False means the pair is not in this project's sourced
        6-pair set — it does NOT mean an interaction has been ruled out. Only
        pairs explicitly marked interaction_present=NO with a documented negative
        search represent a checked absence.
        """
        key = self._make_key(drug_a, drug_b)
        record = self._lookup.get(key)
        if record is None:
            return {
                "pair_found_in_kb": False,
                "drug_a": drug_a, "drug_b": drug_b,
                "note": "Pair not present in knowledge base. This does NOT mean "
                        "an interaction has been ruled out — it means no "
                        "interaction was documented in this project's sourced "
                        "6-pair set. Only pairs marked interaction_present=NO "
                        "with a documented negative search represent a checked "
                        "absence.",
            }
        return {"pair_found_in_kb": True, **record}

    def check_all_pairs(self, drug_list: list) -> list:
        """Check every pairwise combination in a patient's drug list."""
        results = []
        for i in range(len(drug_list)):
            for j in range(i + 1, len(drug_list)):
                results.append(self.check_pair(drug_list[i], drug_list[j]))
        return results
