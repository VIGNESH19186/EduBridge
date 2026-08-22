from tests.conftest import register_and_login


def test_student_analytics_returns_structure_even_with_no_data(client):
    data = register_and_login(client, "student", email="analyticsstudent@example.com")
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    resp = client.get("/api/analytics/student", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert "subject_mastery" in body
    assert "weekly_activity" in body
    assert len(body["weekly_activity"]) == 7  # last 7 days always returned


def test_teacher_dashboard_returns_stats(client):
    data = register_and_login(client, "teacher", email="analyticsteacher@example.com")
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    resp = client.get("/api/teachers/dashboard", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert "total_students" in body
    assert "class_average" in body


def test_teacher_insights_never_makes_unsupported_psychological_claims(client):
    data = register_and_login(client, "teacher", email="insightteacher@example.com")
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    resp = client.get("/api/teachers/insights", headers=headers)
    assert resp.status_code == 200
    insights = resp.json()

    banned_terms = ["depressed", "anxious", "lazy", "unmotivated", "struggling emotionally"]
    for insight in insights:
        combined_text = " ".join(insight["evidence"]) + insight["recommended_intervention"]
        for term in banned_terms:
            assert term not in combined_text.lower()
        # every insight must have measurable evidence backing the risk level
        assert len(insight["evidence"]) > 0
