from app import app


def test_health():
    r = app.test_client().get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_user_found():
    r = app.test_client().get("/user?name=ana")
    assert r.get_json()["users"][0]["role"] == "estudiante"
