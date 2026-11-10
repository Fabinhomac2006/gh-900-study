# novo comentário
import random
import re

from flask import Flask, abort, jsonify, render_template, request
from markupsafe import Markup, escape

from content.flashcards import FLASHCARDS
from content.questions import QUESTIONS, QUESTIONS_BY_ID
from content.topics import OFFICIAL_STUDY_GUIDE, TOPICS, TOPICS_BY_SLUG

MAX_QUIZ_SIZE = 50
DEFAULT_QUIZ_SIZE = 10


def render_inline(text):
    """Converte **negrito** e `código` em HTML, escapando todo o resto."""
    html = str(escape(text))
    html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)
    html = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", html)
    return Markup(html)


def public_question(question):
    return {
        "id": question["id"],
        "topic": question["topic"],
        "text": question["text"],
        "options": question["options"],
        "choose": len(question["answer"]),
    }


def create_app():
    app = Flask(__name__)
    app.jinja_env.filters["inline"] = render_inline

    topic_counts = {
        topic["slug"]: {
            "questions": sum(1 for q in QUESTIONS if q["topic"] == topic["slug"]),
            "cards": sum(1 for c in FLASHCARDS if c["topic"] == topic["slug"]),
        }
        for topic in TOPICS
    }

    @app.context_processor
    def inject_globals():
        return {"all_topics": TOPICS, "study_guide_url": OFFICIAL_STUDY_GUIDE}

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self'; script-src 'self'; frame-ancestors 'none'"
        )
        return response

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("404.html"), 404

    @app.get("/")
    def index():
        return render_template(
            "index.html",
            counts=topic_counts,
            total_questions=len(QUESTIONS),
            total_cards=len(FLASHCARDS),
        )

    @app.get("/topicos")
    def topics():
        return render_template("topics.html", counts=topic_counts)

    @app.get("/topicos/<slug>")
    def topic_detail(slug):
        topic = TOPICS_BY_SLUG.get(slug)
        if topic is None:
            abort(404)
        position = TOPICS.index(topic)
        return render_template(
            "topic.html",
            topic=topic,
            previous=TOPICS[position - 1] if position > 0 else None,
            following=TOPICS[position + 1] if position < len(TOPICS) - 1 else None,
            counts=topic_counts[slug],
        )

    @app.get("/cartoes")
    def flashcards():
        return render_template("flashcards.html")

    @app.get("/quiz")
    def quiz():
        return render_template("quiz.html", counts=topic_counts, total=len(QUESTIONS))

    @app.get("/api/cartoes")
    def api_flashcards():
        topic = request.args.get("topico")
        cards = [c for c in FLASHCARDS if not topic or c["topic"] == topic]
        return jsonify(cards)

    @app.get("/api/questoes")
    def api_questions():
        topic = request.args.get("topico")
        if topic and topic not in TOPICS_BY_SLUG:
            return jsonify(error="Tópico desconhecido."), 400
        size = request.args.get("n", DEFAULT_QUIZ_SIZE, type=int)
        size = max(1, min(size, MAX_QUIZ_SIZE))
        only_ids = request.args.get("ids")
        pool = [q for q in QUESTIONS if not topic or q["topic"] == topic]
        if only_ids:
            wanted = {int(i) for i in only_ids.split(",") if i.strip().isdigit()}
            pool = [q for q in pool if q["id"] in wanted]
        picked = random.sample(pool, min(size, len(pool)))
        return jsonify([public_question(q) for q in picked])

    @app.post("/api/corrigir")
    def api_grade():
        payload = request.get_json(silent=True)
        answers = payload.get("answers") if isinstance(payload, dict) else None
        if not isinstance(answers, dict):
            return jsonify(error="Envie {\"answers\": {id: [indices]}}."), 400

        results = {}
        for raw_id, selected in answers.items():
            question = QUESTIONS_BY_ID.get(int(raw_id)) if str(raw_id).isdigit() else None
            if question is None or not isinstance(selected, list):
                return jsonify(error=f"Resposta inválida para a questão {raw_id}."), 400
            if not all(isinstance(i, int) and not isinstance(i, bool) for i in selected):
                return jsonify(error=f"Índices inválidos para a questão {raw_id}."), 400
            results[str(question["id"])] = {
                "correct": sorted(set(selected)) == sorted(question["answer"]),
                "answer": question["answer"],
                "explanation": question["explanation"],
                "topic": question["topic"],
            }
        return jsonify(results)

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
