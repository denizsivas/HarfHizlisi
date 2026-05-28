"""Flask application factory for HarfHizlisi."""

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from app import game_logic
from app.question_bank import (
    apply_upload,
    example_payload,
    export_categories,
    get_categories,
    reset_to_default,
)
from app.words import TOTAL_QUESTIONS

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


def create_app() -> Flask:
    app = Flask(__name__, static_folder=None)
    CORS(app)

    @app.get("/api/questions")
    def get_questions():
        return jsonify(export_categories())

    @app.get("/api/questions/example")
    def get_questions_example():
        return jsonify(example_payload())

    @app.post("/api/questions/upload")
    def upload_questions():
        body = request.get_json(silent=True)
        if not body:
            return jsonify({"detail": "JSON gövdesi gerekli"}), 400
        try:
            body.setdefault("mode", body.get("mode", "replace"))
            result = apply_upload(body, persist=True)
            return jsonify({"ok": True, **result})
        except ValueError as exc:
            return jsonify({"detail": str(exc)}), 400
        except Exception as exc:
            return jsonify({"detail": f"Geçersiz JSON formatı: {exc}"}), 422

    @app.post("/api/questions/reset")
    def reset_questions():
        categories = reset_to_default()
        return jsonify(
            {
                "ok": True,
                "message": "Varsayılan soru bankası yüklendi",
                "category_count": len(categories),
                "categories": list(categories.keys()),
            }
        )

    @app.get("/api/categories")
    def list_categories():
        return jsonify(
            {
                "categories": [
                    {
                        "id": key,
                        "label": value["label"],
                        "description": value["description"],
                    }
                    for key, value in get_categories().items()
                ]
            }
        )

    @app.post("/api/game/start")
    def api_start_game():
        return jsonify(game_logic.start_game())

    @app.get("/api/game/<game_id>")
    def api_get_game(game_id: str):
        if game_id not in game_logic.games:
            return jsonify({"detail": "Oyun bulunamadı"}), 404
        return jsonify(game_logic.build_game_state(game_id))

    @app.post("/api/game/<game_id>/guess")
    def api_submit_guess(game_id: str):
        body = request.get_json(silent=True) or {}
        guess = (body.get("guess") or "").strip()
        if not guess:
            return jsonify({"detail": "Tahmin boş olamaz"}), 400
        try:
            return jsonify(game_logic.submit_guess(game_id, guess))
        except LookupError as exc:
            return jsonify({"detail": str(exc)}), 404
        except ValueError as exc:
            return jsonify({"detail": str(exc)}), 400

    @app.post("/api/game/<game_id>/timeout")
    def api_timeout_round(game_id: str):
        if game_id not in game_logic.games:
            return jsonify({"detail": "Oyun bulunamadı"}), 404
        game = game_logic.games[game_id]
        if game["game_status"] == "finished":
            return jsonify({"detail": "Oyun bitti"}), 400
        if game["round_status"] != "playing":
            return jsonify({"detail": "Bu tur zaten tamamlandı"}), 400
        if not game_logic.is_round_timed_out(game):
            return jsonify({"detail": "Henüz süre dolmadı"}), 400
        return jsonify(game_logic.fail_round(game_id))

    @app.post("/api/game/<game_id>/next")
    def api_next_question(game_id: str):
        if game_id not in game_logic.games:
            return jsonify({"detail": "Oyun bulunamadı"}), 404
        game = game_logic.games[game_id]
        if game["round_status"] != "completed":
            return jsonify({"detail": "Önce mevcut soruyu cevapla"}), 400
        if game["question_number"] >= TOTAL_QUESTIONS:
            game["game_status"] = "finished"
            return jsonify(game_logic.build_game_state(game_id))
        game["question_number"] += 1
        game_logic.start_round(game)
        return jsonify(game_logic.build_game_state(game_id))

    @app.route("/")
    def index():
        return send_from_directory(STATIC_DIR, "index.html")

    @app.route("/<path:filename>")
    def static_files(filename: str):
        if filename.startswith("api/"):
            return jsonify({"detail": "Not found"}), 404
        target = STATIC_DIR / filename
        if not target.is_file():
            return jsonify({"detail": "Not found"}), 404
        return send_from_directory(STATIC_DIR, filename)

    return app
