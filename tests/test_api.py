from fastapi.testclient import TestClient

from src.api import app


def test_upload_returns_report_and_missing_skills():
    client = TestClient(app)
    response = client.post("/analyse", files={"cv_file": ("cv.txt", b"Python engineer")}, data={"job_text": "Python Docker", "use_llm": "false"})
    assert response.status_code == 200
    assert response.json()["missing_skills"] == ["Docker"]


def test_invalid_upload_returns_actionable_error():
    response = TestClient(app).post("/analyse", files={"cv_file": ("cv.exe", b"bad")}, data={"job_text": "Python", "use_llm": "false"})
    assert response.status_code == 400
