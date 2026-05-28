"""Core HarfHizlisi game state and round logic."""

import random
import uuid
from datetime import datetime, timezone

from app.question_bank import get_categories
from app.validation import answers_match, normalize_guess
from app.words import POINTS_PER_HIDDEN_LETTER, REVEAL_INTERVAL_SECONDS, TOTAL_QUESTIONS

games: dict[str, dict] = {}


def pick_category() -> str:
    return random.choice(list(get_categories().keys()))


def pick_word(game: dict) -> dict[str, str]:
    category = get_categories()[game["category"]]
    question_number = game["question_number"]
    used: set[str] = game.setdefault("used_words", set())

    if question_number == TOTAL_QUESTIONS:
        pool = category["bonus"]
    else:
        length = question_number + 2
        pool = category["words_by_length"][length]

    available = [
        entry
        for entry in pool
        if normalize_guess(entry["word"]) not in used
    ]
    if not available:
        available = pool

    entry = random.choice(available)
    used.add(normalize_guess(entry["word"]))
    return entry


def build_reveal_order(word: str) -> list[int]:
    indices = list(range(len(word)))
    random.shuffle(indices)
    return indices


def revealed_count(elapsed_seconds: float, total_letters: int) -> int:
    if total_letters == 0:
        return 0
    count = int(elapsed_seconds // REVEAL_INTERVAL_SECONDS)
    return min(count, total_letters)


def is_round_timed_out(game: dict) -> bool:
    if game["round_status"] != "playing":
        return False
    elapsed = elapsed_seconds(game["round_started_at"])
    return elapsed >= len(game["word"]) * REVEAL_INTERVAL_SECONDS


def compute_revealed_indices(
    reveal_order: list[int], elapsed_seconds: float
) -> set[int]:
    count = revealed_count(elapsed_seconds, len(reveal_order))
    return set(reveal_order[:count])


def mask_word(word: str, revealed: set[int]) -> str:
    return "".join(ch if i in revealed else "·" for i, ch in enumerate(word))


def hidden_count(word: str, revealed: set[int]) -> int:
    return sum(1 for i in range(len(word)) if i not in revealed)


def question_meta(question_number: int) -> dict:
    is_bonus = question_number == TOTAL_QUESTIONS
    if is_bonus:
        return {
            "question_number": question_number,
            "is_bonus": True,
            "target_length": None,
            "label": "Bonus Soru",
        }
    length = question_number + 2
    return {
        "question_number": question_number,
        "is_bonus": False,
        "target_length": length,
        "label": f"{length} Harfli Kelime",
    }


def elapsed_seconds(started_at: datetime) -> float:
    now = datetime.now(timezone.utc)
    return max(0.0, (now - started_at).total_seconds())


def build_round_state(game: dict) -> dict:
    word = game["word"]
    started_at: datetime = game["round_started_at"]
    elapsed = elapsed_seconds(started_at)
    revealed = compute_revealed_indices(game["reveal_order"], elapsed)
    hidden = hidden_count(word, revealed)
    meta = question_meta(game["question_number"])
    category = get_categories()[game["category"]]

    return {
        **meta,
        "category": game["category"],
        "category_label": category["label"],
        "hint": game["hint"],
        "masked_word": mask_word(word, revealed),
        "word_length": len(word),
        "revealed_count": len(revealed),
        "hidden_count": hidden,
        "potential_points": hidden * POINTS_PER_HIDDEN_LETTER,
        "points_per_hidden_letter": POINTS_PER_HIDDEN_LETTER,
        "reveal_interval_seconds": REVEAL_INTERVAL_SECONDS,
        "seconds_until_next_reveal": max(
            0,
            REVEAL_INTERVAL_SECONDS - (elapsed % REVEAL_INTERVAL_SECONDS),
        )
        if hidden > 0
        else 0,
        "round_elapsed_seconds": round(elapsed, 1),
        "status": game["round_status"],
        "timed_out": is_round_timed_out(game)
        if game["round_status"] == "playing"
        else False,
        "all_revealed": hidden == 0,
        "last_guess": game.get("last_guess"),
        "last_points_awarded": game.get("last_points_awarded"),
        "round_score": game.get("round_score", 0),
    }


def build_game_state(game_id: str) -> dict:
    game = games[game_id]
    category = get_categories()[game["category"]]
    return {
        "game_id": game_id,
        "total_questions": TOTAL_QUESTIONS,
        "total_score": game["total_score"],
        "question_number": game["question_number"],
        "game_status": game["game_status"],
        "category": game["category"],
        "category_label": category["label"],
        "category_description": category["description"],
        "round_history": game.get("round_history", []),
        "round": build_round_state(game),
    }


def start_round(game: dict) -> None:
    entry = pick_word(game)
    word = normalize_guess(entry["word"])
    game["word"] = word
    game["hint"] = entry["hint"]
    game["reveal_order"] = build_reveal_order(word)
    game["round_started_at"] = datetime.now(timezone.utc)
    game["round_status"] = "playing"
    game.pop("last_guess", None)
    game.pop("last_points_awarded", None)
    game.pop("round_score", None)


def record_completed_round(
    game: dict, answered_word: str, points: int, guess: str, *, passed: bool = False
) -> None:
    category = get_categories()[game["category"]]
    history = game.setdefault("round_history", [])
    history.append(
        {
            "question_number": game["question_number"],
            "category": game["category"],
            "category_label": category["label"],
            "word": answered_word,
            "guess": guess,
            "points": points,
            "passed": passed,
            "is_bonus": game["question_number"] == TOTAL_QUESTIONS,
        }
    )


def fail_round(game_id: str) -> dict:
    game = games[game_id]
    answered_word = game["word"]
    game["last_guess"] = None
    game["last_points_awarded"] = 0
    game["round_score"] = 0
    record_completed_round(game, answered_word, 0, "", passed=True)

    if game["question_number"] >= TOTAL_QUESTIONS:
        game["round_status"] = "completed"
        game["game_status"] = "finished"
        return {
            **build_game_state(game_id),
            "timed_out": True,
            "correct": False,
            "points_awarded": 0,
            "revealed_word": answered_word,
            "message": f"Süre doldu. Cevap: {answered_word} (+0 puan). Oyun bitti!",
        }

    game["question_number"] += 1
    start_round(game)
    return {
        **build_game_state(game_id),
        "timed_out": True,
        "correct": False,
        "points_awarded": 0,
        "revealed_word": answered_word,
        "message": f"Süre doldu. Cevap: {answered_word} (+0 puan)",
    }


def start_game() -> dict:
    game_id = str(uuid.uuid4())
    category = pick_category()
    game = {
        "question_number": 1,
        "total_score": 0,
        "game_status": "playing",
        "category": category,
        "used_words": set(),
        "round_history": [],
    }
    start_round(game)
    games[game_id] = game
    return {"game_id": game_id, "state": build_game_state(game_id)}


def submit_guess(game_id: str, guess_raw: str) -> dict:
    if game_id not in games:
        raise LookupError("Oyun bulunamadı")

    game = games[game_id]
    if game["game_status"] == "finished":
        raise ValueError("Oyun bitti")

    if game["round_status"] != "playing":
        raise ValueError("Bu tur zaten tamamlandı")

    if is_round_timed_out(game):
        return fail_round(game_id)

    guess = normalize_guess(guess_raw)
    game["last_guess"] = guess

    if not answers_match(guess_raw, game["word"]):
        return {
            **build_game_state(game_id),
            "correct": False,
            "message": "Yanlış cevap, tekrar dene!",
        }

    elapsed = elapsed_seconds(game["round_started_at"])
    revealed = compute_revealed_indices(game["reveal_order"], elapsed)
    points = hidden_count(game["word"], revealed) * POINTS_PER_HIDDEN_LETTER
    answered_word = game["word"]

    game["total_score"] += points
    record_completed_round(game, answered_word, points, guess)

    if game["question_number"] >= TOTAL_QUESTIONS:
        game["round_status"] = "completed"
        game["round_score"] = points
        game["last_points_awarded"] = points
        game["game_status"] = "finished"
        return {
            **build_game_state(game_id),
            "correct": True,
            "points_awarded": points,
            "message": f"Doğru! +{points} puan. Oyun bitti!",
            "revealed_word": answered_word,
        }

    game["question_number"] += 1
    start_round(game)

    return {
        **build_game_state(game_id),
        "correct": True,
        "points_awarded": points,
        "message": f"Doğru! +{points} puan",
        "revealed_word": answered_word,
    }
