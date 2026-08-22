from tests.conftest import register_and_login


def test_ask_doubt_returns_grounded_or_honest_response(client):
    data = register_and_login(client, "student", email="doubtstudent@example.com")
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    resp = client.post(
        "/api/doubts",
        json={"question_text": "Why does differentiation of x squared become 2x?", "language": "English"},
        headers=headers,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["detected_subject"] in ("Mathematics", "General")
    assert "quick_check_question" in body
    assert isinstance(body["citations"], list)
    # grounded flag must be a real boolean, and if False, explanation must be the honest fallback
    if not body["grounded"]:
        assert "couldn't find enough information" in body["explanation"]


def test_ask_doubt_requires_auth(client):
    resp = client.post("/api/doubts", json={"question_text": "What is a fraction?"})
    assert resp.status_code == 401


def test_doubt_history_returns_list(client):
    data = register_and_login(client, "student", email="doubthistory@example.com")
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    client.post("/api/doubts", json={"question_text": "What is a fraction?"}, headers=headers)

    resp = client.get("/api/doubts/history", headers=headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1
