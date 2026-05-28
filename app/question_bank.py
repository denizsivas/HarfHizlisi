"""Mutable question bank with JSON upload support."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.validation import normalize_guess

DEFAULT_CATEGORIES: dict[str, dict]
_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "questions.json"

_categories: dict[str, dict] | None = None


def _load_default_from_words_module() -> dict[str, dict]:
    from app.words import CATEGORIES

    return CATEGORIES


def get_categories() -> dict[str, dict]:
    global _categories
    if _categories is None:
        _categories = _load_persisted_or_default()
    return _categories


def _load_persisted_or_default() -> dict[str, dict]:
    if _DATA_FILE.exists():
        try:
            payload = json.loads(_DATA_FILE.read_text(encoding="utf-8"))
            return validate_question_payload(payload)["categories"]
        except (json.JSONDecodeError, ValueError):
            pass
    return _load_default_from_words_module()


def reset_to_default() -> dict[str, dict]:
    global _categories
    _categories = _load_default_from_words_module()
    if _DATA_FILE.exists():
        _DATA_FILE.unlink()
    return _categories


class WordEntry(BaseModel):
    word: str = Field(min_length=1, max_length=64)
    hint: str = Field(min_length=1, max_length=500)


class CategoryPayload(BaseModel):
    label: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=200)
    words_by_length: dict[str, list[WordEntry]] = Field(default_factory=dict)
    bonus: list[WordEntry] = Field(default_factory=list)

    @field_validator("words_by_length")
    @classmethod
    def keys_must_be_lengths(cls, value: dict[str, list[WordEntry]]) -> dict[str, list[WordEntry]]:
        for key in value:
            if not key.isdigit() or not (3 <= int(key) <= 9):
                raise ValueError(
                    f"words_by_length anahtarı 3-9 arası olmalı, geçersiz: {key!r}"
                )
        return value


class QuestionUploadPayload(BaseModel):
    """JSON gövdesi: kategoriler ve kelimeler."""

    mode: str = Field(default="replace", pattern="^(replace|merge)$")
    categories: dict[str, CategoryPayload]


_CATEGORY_ID_RE = re.compile(r"^[a-z0-9_]+$", re.IGNORECASE)


def _normalize_category_entry(category_id: str, payload: CategoryPayload) -> dict:
    if not _CATEGORY_ID_RE.match(category_id):
        raise ValueError(
            f"Geçersiz kategori id: {category_id!r} (yalnızca harf, rakam, alt çizgi)"
        )

    words_by_length: dict[int, list[dict[str, str]]] = {}
    seen_words: set[str] = set()

    for length_key, entries in payload.words_by_length.items():
        length = int(length_key)
        bucket: list[dict[str, str]] = []
        for entry in entries:
            word = normalize_guess(entry.word)
            if len(word) != length:
                raise ValueError(
                    f"[{category_id}] '{entry.word}' {length} harfli grupta "
                    f"olamaz (gerçek uzunluk: {len(word)})"
                )
            if word in seen_words:
                continue
            seen_words.add(word)
            bucket.append({"word": word, "hint": entry.hint.strip()})
        if bucket:
            words_by_length[length] = bucket

    for length in range(3, 10):
        if length not in words_by_length or len(words_by_length[length]) < 1:
            raise ValueError(
                f"[{category_id}] {length} harfli en az bir kelime gerekli"
            )

    bonus: list[dict[str, str]] = []
    for entry in payload.bonus:
        word = normalize_guess(entry.word)
        if len(word) < 3:
            raise ValueError(f"[{category_id}] bonus kelime çok kısa: {entry.word!r}")
        if word in seen_words:
            continue
        seen_words.add(word)
        bonus.append({"word": word, "hint": entry.hint.strip()})

    if len(bonus) < 1:
        raise ValueError(f"[{category_id}] en az bir bonus kelime gerekli")

    return {
        "label": payload.label.strip(),
        "description": payload.description.strip(),
        "words_by_length": words_by_length,
        "bonus": bonus,
    }


def validate_question_payload(data: dict[str, Any]) -> dict[str, Any]:
    """Ham dict doğrula ve normalize edilmiş kategori sözlüğü döndür."""
    if "categories" not in data:
        raise ValueError("JSON içinde 'categories' alanı zorunlu")

    upload = QuestionUploadPayload.model_validate(data)
    normalized: dict[str, dict] = {}

    for category_id, category_payload in upload.categories.items():
        normalized[category_id] = _normalize_category_entry(
            category_id, category_payload
        )

    if not normalized:
        raise ValueError("En az bir kategori gerekli")

    return {"mode": upload.mode, "categories": normalized}


def apply_upload(data: dict[str, Any], *, persist: bool = True) -> dict[str, Any]:
    global _categories
    parsed = validate_question_payload(data)
    mode = parsed["mode"]
    incoming = parsed["categories"]

    if mode == "replace":
        _categories = incoming
    else:
        current = get_categories().copy()
        current.update(incoming)
        _categories = current

    if persist:
        _persist(_categories)

    return {
        "mode": mode,
        "category_count": len(_categories),
        "categories": list(_categories.keys()),
    }


def _persist(categories: dict[str, dict]) -> None:
    _DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    serializable = {
        "mode": "replace",
        "categories": {
            cat_id: {
                "label": cat["label"],
                "description": cat["description"],
                "words_by_length": {
                    str(length): cat["words_by_length"][length]
                    for length in sorted(cat["words_by_length"])
                },
                "bonus": cat["bonus"],
            }
            for cat_id, cat in categories.items()
        },
    }
    _DATA_FILE.write_text(
        json.dumps(serializable, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def export_categories() -> dict[str, Any]:
    categories = get_categories()
    return {
        "mode": "replace",
        "categories": {
            cat_id: {
                "label": cat["label"],
                "description": cat["description"],
                "words_by_length": {
                    str(length): cat["words_by_length"][length]
                    for length in sorted(cat["words_by_length"])
                },
                "bonus": cat["bonus"],
            }
            for cat_id, cat in categories.items()
        },
    }


def example_payload() -> dict[str, Any]:
    return {
        "mode": "replace",
        "categories": {
            "ornek": {
                "label": "Örnek",
                "description": "Yüklediğiniz soru seti için şablon",
                "words_by_length": {
                    "3": [{"word": "GÜL", "hint": "Kokulu bir çiçek"}],
                    "4": [{"word": "KEDİ", "hint": "Miyavlayan ev hayvanı"}],
                    "5": [{"word": "KALEM", "hint": "Yazı yazmaya yarayan araç"}],
                    "6": [{"word": "HEYKEL", "hint": "Üç boyutlu sanat eseri"}],
                    "7": [{"word": "OKYANUS", "hint": "Dünyanın en büyük su kütlesi"}],
                    "8": [{"word": "İSTANBUL", "hint": "Boğaz'ın iki yakasında kurulu şehir"}],
                    "9": [{"word": "KÜTÜPHANE", "hint": "Kitapların bulunduğu sessiz yer"}],
                },
                "bonus": [
                    {
                        "word": "FOTOĞRAFÇILIK",
                        "hint": "Işık ve gölgeyle an yakalama sanatı",
                    }
                ],
            }
        },
    }
