import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402
from content.flashcards import FLASHCARDS  # noqa: E402
from content.questions import QUESTIONS  # noqa: E402
from content.topics import TOPICS, TOPICS_BY_SLUG  # noqa: E402


class ContentTests(unittest.TestCase):
    def test_questions_are_consistent(self):
        ids = [q["id"] for q in QUESTIONS]
        self.assertEqual(len(ids), len(set(ids)))
        for q in QUESTIONS:
            with self.subTest(question=q["id"]):
                self.assertIn(q["topic"], TOPICS_BY_SLUG)
                self.assertGreaterEqual(len(q["options"]), 2)
                self.assertEqual(len(q["options"]), len(set(q["options"])))
                self.assertTrue(q["answer"])
                self.assertTrue(all(0 <= a < len(q["options"]) for a in q["answer"]))
                self.assertEqual(len(q["answer"]), len(set(q["answer"])))
                self.assertTrue(q["explanation"])

    def test_every_topic_has_questions_and_cards(self):
        for topic in TOPICS:
            with self.subTest(topic=topic["slug"]):
                self.assertTrue(any(q["topic"] == topic["slug"] for q in QUESTIONS))
                self.assertTrue(any(c["topic"] == topic["slug"] for c in FLASHCARDS))

    def test_flashcards_reference_valid_topics(self):
        self.assertTrue(all(c["topic"] in TOPICS_BY_SLUG for c in FLASHCARDS))


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_pages_render(self):
        paths = ["/", "/topicos", "/cartoes", "/quiz"] + [f"/topicos/{t['slug']}" for t in TOPICS]
        for path in paths:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_unknown_topic_is_404(self):
        self.assertEqual(self.client.get("/topicos/nao-existe").status_code, 404)

    def test_questions_api_hides_answers(self):
        data = self.client.get("/api/questoes?n=5").get_json()
        self.assertEqual(len(data), 5)
        for q in data:
            self.assertNotIn("answer", q)
            self.assertNotIn("explanation", q)

    def test_questions_api_filters_topic_and_validates(self):
        data = self.client.get("/api/questoes?topico=comunidade&n=50").get_json()
        self.assertTrue(data and all(q["topic"] == "comunidade" for q in data))
        self.assertEqual(self.client.get("/api/questoes?topico=xyz").status_code, 400)

    def test_grading(self):
        multi = next(q for q in QUESTIONS if len(q["answer"]) > 1)
        single = next(q for q in QUESTIONS if len(q["answer"]) == 1)
        wrong = (single["answer"][0] + 1) % len(single["options"])
        response = self.client.post(
            "/api/corrigir",
            json={"answers": {str(multi["id"]): list(reversed(multi["answer"])), str(single["id"]): [wrong]}},
        )
        body = response.get_json()
        self.assertTrue(body[str(multi["id"])]["correct"])
        self.assertFalse(body[str(single["id"])]["correct"])

    def test_grading_rejects_bad_payloads(self):
        for payload in ({}, {"answers": []}, {"answers": {"9999": [0]}}, {"answers": {"1": ["a"]}}):
            with self.subTest(payload=payload):
                self.assertEqual(self.client.post("/api/corrigir", json=payload).status_code, 400)

    def test_inline_rendering_escapes_html(self):
        from app import render_inline

        self.assertEqual(str(render_inline("<b>**x**</b>")), "&lt;b&gt;<strong>x</strong>&lt;/b&gt;")


if __name__ == "__main__":
    unittest.main()
