import json
from pathlib import Path

import pytest

from app.question_bank import apply_upload, example_payload, reset_to_default, validate_question_payload


def test_example_payload_validates():
    result = validate_question_payload(example_payload())
    assert "ornek" in result["categories"]
    assert 3 in result["categories"]["ornek"]["words_by_length"]


def test_rejects_wrong_length():
    payload = example_payload()
    payload["categories"]["ornek"]["words_by_length"]["3"][0]["word"] = "KEDİ"
    with pytest.raises(ValueError, match="3 harfli"):
        validate_question_payload(payload)


def test_upload_replace_and_reset():
    reset_to_default()
    result = apply_upload(example_payload(), persist=False)
    assert result["category_count"] >= 1
    assert "ornek" in result["categories"]

    reset_to_default()


def test_example_file_matches_schema():
    path = Path(__file__).resolve().parent.parent / "examples" / "questions.example.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    validate_question_payload(data)
