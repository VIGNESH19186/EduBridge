from tests.conftest import register_and_login


def test_register_creates_student(client):
    data = register_and_login(client, "student")
    assert data["role"] == "student"
    assert "access_token" in data


def test_register_duplicate_email_rejected(client):
    data = register_and_login(client, "student")
    email = data["name"]  # not used; re-register same email explicitly
    payload = {"name": "Dup", "email": "dup@example.com", "password": "password123", "role": "student"}
    r1 = client.post("/api/auth/register", json=payload)
    assert r1.status_code == 200
    r2 = client.post("/api/auth/register", json=payload)
    assert r2.status_code == 400


def test_login_success(client):
    payload = {"name": "Login Test", "email": "logintest@example.com", "password": "password123", "role": "student"}
    client.post("/api/auth/register", json=payload)
    resp = client.post("/api/auth/login", json={"email": payload["email"], "password": payload["password"]})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password_rejected(client):
    payload = {"name": "Login Wrong", "email": "loginwrong@example.com", "password": "password123", "role": "student"}
    client.post("/api/auth/register", json=payload)
    resp = client.post("/api/auth/login", json={"email": payload["email"], "password": "wrongpass"})
    assert resp.status_code == 401


def test_me_requires_token(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


def test_me_returns_user_with_valid_token(client):
    data = register_and_login(client, "student", email="metest@example.com")
    resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {data['access_token']}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "metest@example.com"


def test_student_cannot_access_teacher_routes(client):
    data = register_and_login(client, "student", email="rbacstudent@example.com")
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    resp = client.get("/api/teachers/dashboard", headers=headers)
    assert resp.status_code == 403


def test_teacher_can_access_teacher_routes(client):
    data = register_and_login(client, "teacher", email="rbacteacher@example.com")
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    resp = client.get("/api/teachers/dashboard", headers=headers)
    assert resp.status_code == 200


def test_teacher_cannot_access_student_only_routes(client):
    data = register_and_login(client, "teacher", email="rbacteacher2@example.com")
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    resp = client.get("/api/students/me", headers=headers)
    assert resp.status_code == 403

