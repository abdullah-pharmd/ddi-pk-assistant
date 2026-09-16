"""Tests for src/ddi_engine.py."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ddi_engine import DDIEngine

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "ddi_knowledge_base.csv")


def test_known_pair_found():
    engine = DDIEngine(DATA_PATH)
    result = engine.check_pair("Vancomycin", "Gentamicin")
    assert result["pair_found_in_kb"] is True
    assert result["severity"] == "High"


def test_reversed_order_same_result():
    engine = DDIEngine(DATA_PATH)
    forward = engine.check_pair("Vancomycin", "Gentamicin")
    reversed_ = engine.check_pair("Gentamicin", "Vancomycin")
    assert forward["severity"] == reversed_["severity"]


def test_unknown_pair_not_confused_with_confirmed_negative():
    engine = DDIEngine(DATA_PATH)
    result = engine.check_pair("Vancomycin", "Ibuprofen")
    assert result["pair_found_in_kb"] is False
    assert "does NOT mean" in result["note"]


def test_confirmed_negative_pair():
    engine = DDIEngine(DATA_PATH)
    result = engine.check_pair("Gentamicin", "Phenytoin")
    assert result["pair_found_in_kb"] is True
    assert result["interaction_present"] == "NO"


def test_check_all_pairs_covers_full_combination():
    engine = DDIEngine(DATA_PATH)
    results = engine.check_all_pairs(["Vancomycin", "Gentamicin", "Digoxin"])
    assert len(results) == 3  # 3 choose 2
