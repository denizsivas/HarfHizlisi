"""Tests for Turkish case-insensitive answer matching."""

from app.validation import answers_match, normalize_guess


def test_lowercase_matches_uppercase():
    assert answers_match("gül", "GÜL")
    assert answers_match("GÜL", "gül")


def test_turkish_i_dotless():
    assert answers_match("ışık", "IŞIK")
    assert answers_match("izmir", "İZMİR")


def test_whitespace_is_ignored():
    assert answers_match("  karadeniz  ", "KARADENİZ")


def test_punctuation_is_ignored():
    assert answers_match("lozan antlaşması", "LOZANANTLAŞMASI")
    assert answers_match("lozan-antlaşması", "LOZANANTLAŞMASI")
    assert answers_match("lozan'antlaşması", "LOZANANTLAŞMASI")


def test_normalize_uppercases_turkish():
    assert normalize_guess("iğne") == "İĞNE"
    assert normalize_guess("ırmak") == "IRMAK"
