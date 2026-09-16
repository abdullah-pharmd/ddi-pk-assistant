"""
Batch Prediction — CSV upload processing.
Format: one row per patient-drug combination, grouped by patient_id before
running the full renal -> PK -> DDI -> dose-adjustment pipeline per patient.
"""
import csv
import io
from collections import defaultdict

REQUIRED_COLUMNS = {"patient_id", "age", "sex", "weight_kg", "height_cm",
                     "scr_mg_dl", "hepatic_impairment", "drug", "nyha_class"}
VALID_DRUGS = {"Gentamicin", "Vancomycin", "Digoxin", "Phenytoin"}


def validate_csv_rows(rows: list) -> list:
    """
    Validates rows before processing. Returns a list of error strings — empty
    list means the CSV is valid. Does NOT process/calculate anything itself.
    """
    errors = []
    if not rows:
        return ["CSV is empty."]

    missing_cols = REQUIRED_COLUMNS - set(rows[0].keys())
    if missing_cols:
        errors.append(f"Missing required column(s): {', '.join(sorted(missing_cols))}")
        return errors  # can't validate rows meaningfully without the columns

    for i, row in enumerate(rows, start=2):  # start=2 accounts for header row
        line = f"Row {i} (patient_id={row.get('patient_id', '?')})"
        if not row.get("patient_id", "").strip():
            errors.append(f"{line}: missing patient_id")
        try:
            age = int(row["age"])
            if age <= 0 or age > 130:
                errors.append(f"{line}: implausible age '{row['age']}'")
        except (ValueError, KeyError):
            errors.append(f"{line}: invalid or missing age")
        try:
            weight = float(row["weight_kg"])
            if weight <= 0:
                errors.append(f"{line}: weight_kg must be positive")
        except (ValueError, KeyError):
            errors.append(f"{line}: invalid or missing weight_kg")
        try:
            scr = float(row["scr_mg_dl"])
            if scr <= 0:
                errors.append(f"{line}: scr_mg_dl must be positive")
        except (ValueError, KeyError):
            errors.append(f"{line}: invalid or missing scr_mg_dl")
        if row.get("sex", "").strip().lower() not in ("male", "female"):
            errors.append(f"{line}: sex must be 'male' or 'female'")
        drug = row.get("drug", "").strip()
        if drug not in VALID_DRUGS:
            errors.append(f"{line}: drug '{drug}' not in this project's scope "
                           f"({', '.join(sorted(VALID_DRUGS))})")
        if drug == "Digoxin" and row.get("nyha_class", "").strip() not in ("I", "II", "III", "IV"):
            errors.append(f"{line}: Digoxin requires a valid nyha_class (I-IV)")

    return errors


def group_by_patient(rows: list) -> dict:
    """Groups flat CSV rows into one record per patient_id with a drug list."""
    patients = defaultdict(lambda: {"drugs": [], "nyha_class": None})
    for row in rows:
        pid = row["patient_id"].strip()
        patients[pid]["age"] = int(row["age"])
        patients[pid]["sex"] = row["sex"].strip().lower()
        patients[pid]["weight_kg"] = float(row["weight_kg"])
        patients[pid]["height_cm"] = float(row["height_cm"])
        patients[pid]["scr_mg_dl"] = float(row["scr_mg_dl"])
        patients[pid]["hepatic_impairment"] = row["hepatic_impairment"].strip().lower() == "yes"
        patients[pid]["drugs"].append(row["drug"].strip())
        if row["drug"].strip() == "Digoxin":
            patients[pid]["nyha_class"] = row["nyha_class"].strip()
    return dict(patients)


def parse_csv_text(csv_text: str) -> list:
    """Parses uploaded CSV text into a list of row dicts."""
    return list(csv.DictReader(io.StringIO(csv_text)))


def results_to_csv(results: list) -> str:
    """Flattens batch results back into a downloadable CSV string."""
    if not results:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
    return output.getvalue()
