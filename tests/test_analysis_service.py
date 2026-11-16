
from pathlib import Path

from app.services.analysis_service import analyse_log_file


SAMPLE_FILE = (
    Path(__file__).parent.parent
    / "data"
    / "samples"
    / "authentication_events.json"
)


def test_analysis_service():
    result = analyse_log_file(SAMPLE_FILE)

    assert result["total_events"] == 6
    assert result["total_alerts"] == 1
    assert len(result["events"]) == 6
    assert result["alerts"][0]["rule_id"] == "AUTH-001"
