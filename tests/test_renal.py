"""Tests for src/renal.py."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from renal import crcl_cockcroft_gault, renal_category, calculate_ibw


def test_normal_weight_patient():
    result = crcl_cockcroft_gault(age=65, actual_weight_kg=70, height_cm=175, sex="male", scr_mg_dl=1.0)
    assert result["crcl_ml_min"] == pytest.approx(72.9, abs=0.5)
    assert result["weight_basis"] == "actual (below IBW)"


def test_obese_patient_uses_adjusted_weight():
    result = crcl_cockcroft_gault(age=65, actual_weight_kg=110, height_cm=175, sex="male", scr_mg_dl=1.0)
    assert result["weight_basis"] == "adjusted body weight (obesity correction)"
    assert result["crcl_ml_min"] == pytest.approx(89.9, abs=0.5)


def test_renal_category_boundaries():
    assert renal_category(90)["category"] == "Normal"
    assert renal_category(89.9)["category"] == "Mild"
    assert renal_category(60)["category"] == "Mild"
    assert renal_category(59.9)["category"] == "Moderate"
    assert renal_category(30)["category"] == "Moderate"
    assert renal_category(29.9)["category"] == "Severe"


def test_zero_scr_raises():
    with pytest.raises(ValueError):
        crcl_cockcroft_gault(age=65, actual_weight_kg=70, height_cm=175, sex="male", scr_mg_dl=0)


def test_negative_age_raises():
    with pytest.raises(ValueError):
        crcl_cockcroft_gault(age=-5, actual_weight_kg=70, height_cm=175, sex="male", scr_mg_dl=1.0)


def test_zero_weight_raises():
    with pytest.raises(ValueError):
        crcl_cockcroft_gault(age=65, actual_weight_kg=0, height_cm=175, sex="male", scr_mg_dl=1.0)


def test_invalid_sex_raises():
    with pytest.raises(ValueError):
        crcl_cockcroft_gault(age=65, actual_weight_kg=70, height_cm=175, sex="other", scr_mg_dl=1.0)


def test_negative_crcl_category_raises():
    with pytest.raises(ValueError):
        renal_category(-5)
