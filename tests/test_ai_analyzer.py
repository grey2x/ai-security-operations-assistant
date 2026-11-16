
import pytest
from types import SimpleNamespace

from app.services.ai_analyzer import analyse_alert


class MockCompletions:
    def create(self, **kwargs):
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content="Five failed login attempts were detected from one IP address."
                    )
                )
            ]
        )


class MockChat:
    def __init__(self):
        self.completions = MockCompletions()


class MockClient:
    def __init__(self):
        self.chat = MockChat()


@pytest.fixture(autouse=True)
def configure_test_environment(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_MODEL", "test-model")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)


def test_analyse_alert_with_mock_client():
    alert = {
        "rule_id": "AUTH-001",
        "title": "Repeated failed login attempts",
        "severity": "high",
        "source_ip": "192.0.2.15",
        "failed_attempts": 5,
        "threshold": 5,
        "window_minutes": 5,
        "usernames": ["admin"],
    }

    result = analyse_alert(alert, client=MockClient())

    assert "Five failed login attempts" in result
