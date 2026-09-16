"""
Tests for src/pk_engine.py. Cases V1/V2/D1/D2 are REAL literature-sourced
validation cases (Bauer LA, Applied Clinical Pharmacokinetics, 2nd ed.,
Ch.5 Examples 1-2, Ch.6 Examples 1&3). See data/validation_cases.csv.
Patient in all four cases: 70kg, 5'10" (177.8cm), male -- IBW=73kg (not obese).
"""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from pk_engine import gentamicin_pk, vancomycin_pk, digoxin_pk, phenytoin_pk, winter_tozer_correction

HEIGHT_5FT10 = 177.8


def test_vancomycin_case_v1_normal_renal_function():
    result = vancomycin_pk(weight_kg=70, crcl_ml_min=97, height_cm=HEIGHT_5FT10, sex="male")
    assert result["vd_l"] == pytest.approx(49.0, abs=0.1)
    assert result["half_life_hr"] == pytest.approx(8.0, abs=0.2)


def test_vancomycin_case_v2_renal_impairment():
    result = vancomycin_pk(weight_kg=70, crcl_ml_min=25, height_cm=HEIGHT_5FT10, sex="male")
    assert result["half_life_hr"] == pytest.approx(27.0, abs=0.3)


def test_vancomycin_nonrenal_constant_scales_with_weight():
    """Regression test: nonrenal constant must scale with weight_kg (0.05*weight),
    NOT stay flat at +0.05 mL/min. Flat form would give cl_ml_min ~= 17.4 (WRONG)."""
    result = vancomycin_pk(weight_kg=70, crcl_ml_min=25, height_cm=HEIGHT_5FT10, sex="male")
    assert result["cl_ml_min"] == pytest.approx(20.88, abs=0.1)
    assert result["cl_ml_min"] != pytest.approx(17.43, abs=0.1)


def test_vancomycin_obesity_vd_correction_uses_ibw_not_actual():
    """Regression test: for a genuinely obese patient (>30% over IBW), Vd must
    use IBW, not actual weight. An earlier draft applied IBW unconditionally,
    which broke the non-obese validation cases above -- this test guards both
    directions: obesity correction triggers ONLY when it should."""
    result = vancomycin_pk(weight_kg=130, crcl_ml_min=60, height_cm=HEIGHT_5FT10, sex="male")
    assert result["weight_used_for_vd_kg"] == pytest.approx(73.0, abs=0.5)  # IBW, not 130


def test_vancomycin_non_obese_uses_actual_weight_not_ibw():
    """Guards the opposite direction: a non-obese patient (70kg actual vs 73kg
    IBW) must use actual weight for Vd, not IBW."""
    result = vancomycin_pk(weight_kg=70, crcl_ml_min=97, height_cm=HEIGHT_5FT10, sex="male")
    assert result["weight_used_for_vd_kg"] == pytest.approx(70.0, abs=0.5)  # actual, not 73 IBW


def test_digoxin_case_d1_normal_renal_no_hf():
    result = digoxin_pk(weight_kg=70, crcl_ml_min=97, nyha_class="II", height_cm=HEIGHT_5FT10, sex="male")
    assert result["cl_ml_min"] == pytest.approx(167, abs=2)
    assert result["vd_l"] == pytest.approx(490, abs=1)


def test_digoxin_case_d2_renal_impairment_moderate_hf():
    result = digoxin_pk(weight_kg=70, crcl_ml_min=25, nyha_class="IV", height_cm=HEIGHT_5FT10, sex="male")
    assert result["cl_ml_min"] == pytest.approx(53, abs=1)


def test_digoxin_invalid_nyha_class_raises():
    with pytest.raises(ValueError):
        digoxin_pk(weight_kg=70, crcl_ml_min=80, nyha_class="V", height_cm=HEIGHT_5FT10, sex="male")


def test_gentamicin_normal_renal_function():
    result = gentamicin_pk(weight_kg=70, crcl_ml_min=80, height_cm=HEIGHT_5FT10, sex="male")
    assert result["half_life_hr"] == pytest.approx(2.79, abs=0.05)


def test_phenytoin_dose_for_target_css():
    result = phenytoin_pk(weight_kg=70, css_target_mg_l=15.0, height_cm=HEIGHT_5FT10, sex="male")
    # NOTE: now uses IBW-conditional weight for Vmax -- for this non-obese patient,
    # weight_for_vmax = actual = 70kg, same as before the weight-basis fix
    assert result["dose_mg_day"] == pytest.approx(386.8, abs=1.0)


def test_phenytoin_target_at_or_above_vmax_raises():
    with pytest.raises(ValueError):
        phenytoin_pk(weight_kg=70, css_target_mg_l=1000.0, height_cm=HEIGHT_5FT10, sex="male")


def test_winter_tozer_hypoalbuminemia_correction():
    result = winter_tozer_correction(8.0, 2.5, severe_renal_impairment=False)
    assert result["c_corrected_mg_l"] == pytest.approx(13.33, abs=0.05)


def test_zero_weight_raises():
    with pytest.raises(ValueError):
        vancomycin_pk(weight_kg=0, crcl_ml_min=80, height_cm=HEIGHT_5FT10, sex="male")
