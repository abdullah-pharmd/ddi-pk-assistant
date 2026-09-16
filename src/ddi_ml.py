"""
Module 3 (ML side) — DDI Severity Audit Classifier
Per docs/ml_component_design.md: this is an EXPLAINABILITY/AUDIT tool on the
6-row DDI knowledge base, NOT a validated predictor. No train/test split, no
cross-validation performance claim (singleton "High" class makes both
structurally uninformative -- see docs/model_validation_design.md).
Every function here must be used with the UI wording rules from
docs/shap_explainability_design.md -- literature severity is always primary/
headline; this module's output is always a supplementary audit panel.
"""
import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder


FEATURE_COLUMNS = ["interaction_category", "interaction_type", "pathway", "evidence_level"]
TARGET_COLUMN = "severity"


def load_kb_for_ml(csv_path: str) -> tuple:
    """Loads the KB and returns (feature_dicts, labels) for encoding."""
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    features = [{col: row.get(col, "unknown") for col in FEATURE_COLUMNS} for row in rows]
    labels = [row[TARGET_COLUMN] for row in rows]
    pair_labels = [f"{row['drug_a']}+{row['drug_b']}" for row in rows]
    return features, labels, pair_labels


def train_audit_model(csv_path: str, random_state: int = 42):
    """
    Trains a Random Forest on the FULL 6-row KB (no held-out test set -- see
    docs/model_validation_design.md for why). Fixed conservative hyperparameters
    per docs/coding_strategy.md's reproducibility rule (random_state fixed).
    Returns (model, encoder, X_encoded, labels, pair_labels, feature_names) for
    downstream SHAP use.
    """
    features, labels, pair_labels = load_kb_for_ml(csv_path)
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    X = encoder.fit_transform([[f[col] for col in FEATURE_COLUMNS] for f in features])
    feature_names = encoder.get_feature_names_out(FEATURE_COLUMNS)

    model = RandomForestClassifier(n_estimators=50, max_depth=3, random_state=random_state)
    model.fit(X, labels)
    return model, encoder, X, labels, pair_labels, feature_names


def majority_baseline(labels: list) -> dict:
    """
    Descriptive comparison point only -- per docs/model_validation_design.md,
    NOT a performance claim, just context for the fitted model's training-set fit.
    """
    from collections import Counter
    counts = Counter(labels)
    majority_class, majority_count = counts.most_common(1)[0]
    return {
        "majority_class": majority_class,
        "baseline_accuracy": round(majority_count / len(labels), 3),
        "note": "Descriptive baseline only -- achieved by always predicting the "
                "most common label, using no information. Not a performance metric.",
    }


def audit_fit_summary(model, X, labels) -> dict:
    """
    Training-set fit ONLY -- explicitly NOT a generalization/test-performance
    claim (docs/model_validation_design.md). Confusion matrix here shows whether
    the model's fit is internally consistent with its own training labels, not
    whether it would classify an unseen pair correctly.
    """
    from sklearn.metrics import confusion_matrix
    predictions = model.predict(X)
    classes = sorted(set(labels))
    cm = confusion_matrix(labels, predictions, labels=classes)
    return {
        "classes": classes,
        "confusion_matrix": cm.tolist(),
        "note": "TRAINING-SET FIT ONLY. Not a test-set or cross-validated result. "
                "See docs/model_validation_design.md for why cross-validation is "
                "structurally uninformative on this dataset (singleton High class).",
    }
