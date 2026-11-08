from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_sample_demo_executes_the_full_ui_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=30).run()
    assert not app.exception
    app.button[0].click().run()
    assert not app.exception
    assert len(app.metric) == 4
    assert app.session_state["report"].skill_evidence
