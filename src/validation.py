"""
Module — Literature Validation Comparison
Compares tool output against real, cited literature/textbook worked examples.
Does NOT generate or assume any case data itself — operates only on rows
supplied in data/validation_cases.csv (currently empty; see
docs/validation_framework.md for what's needed to populate it).
"""


def numerical_error(calculated: float, reported: float) -> dict:
    """
    Percent error of a calculated PK value against a reported literature value.
    Source-agnostic — caller supplies both values and cites where 'reported'
    came from.
    """
    if reported == 0:
        raise ValueError("reported value cannot be zero (division by zero)")
    pct_error = ((calculated - reported) / reported) * 100
    return {
        "calculated": calculated, "reported": reported,
        "pct_error": round(pct_error, 1),
        "direction": "overestimate" if pct_error > 0 else "underestimate",
    }


def categorical_agreement(calculated_category: str, reported_category: str) -> dict:
    """
    For categorical results (DDI severity, renal category) — simple match/mismatch,
    reported plainly rather than as a percentage given small case counts.
    """
    return {
        "calculated": calculated_category, "reported": reported_category,
        "match": calculated_category == reported_category,
    }


def summarize_validation_run(results: list) -> dict:
    """
    Aggregates a list of numerical_error/categorical_agreement results into a
    plain-language summary — explicitly avoids computing precision/recall/ROC-type
    metrics, which would overstate confidence given the small case counts expected
    (see docs/validation_framework.md, Section 2).
    """
    numeric_results = [r for r in results if "pct_error" in r]
    categorical_results = [r for r in results if "match" in r]

    summary = {"total_cases": len(results)}
    if numeric_results:
        errors = [abs(r["pct_error"]) for r in numeric_results]
        summary["numeric_cases"] = len(numeric_results)
        summary["mean_abs_pct_error"] = round(sum(errors) / len(errors), 1)
        summary["max_abs_pct_error"] = round(max(errors), 1)
    if categorical_results:
        matches = sum(1 for r in categorical_results if r["match"])
        summary["categorical_cases"] = len(categorical_results)
        summary["categorical_matches"] = f"{matches} of {len(categorical_results)}"
    return summary
