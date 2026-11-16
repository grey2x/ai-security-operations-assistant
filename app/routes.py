
from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request
)

from openai import APIError, APITimeoutError

from app.services.ai_analyzer import analyse_alert
from app.services.analysis_service import analyse_log_file
from app.services.database import save_incident, get_incidents


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/health")
def health():
    return jsonify({
        "status": "online",
        "application": "AI Security Operations Assistant",
        "version": "1.0.0"
    })


@main.route("/api/analyse-samples", methods=["GET"])
def analyse_samples():
    sample_file = (
        Path(__file__).parent.parent
        / "data"
        / "samples"
        / "authentication_events.json"
    )

    try:
        results = analyse_log_file(sample_file)

        for alert in results["alerts"]:
            save_incident(alert)

        return jsonify({
            "total_events": results["total_events"],
            "total_alerts": results["total_alerts"],
            "alerts": results["alerts"]
        })

    except (ValueError, OSError) as error:
        current_app.logger.exception("Sample analysis failed.")

        return jsonify({
            "error": str(error)
        }), 400


@main.route("/api/ai-analysis", methods=["POST"])
def ai_analysis():
    alert = request.get_json(silent=True)

    if not isinstance(alert, dict):
        return jsonify({
            "error": "Invalid incident data."
        }), 400

    try:
        explanation = analyse_alert(alert)

        return jsonify({
            "status": "success",
            "analysis": explanation
        })

    except APITimeoutError:
        current_app.logger.exception("AI provider request timed out.")

        return jsonify({
            "error": "The AI provider took too long to respond. Please try again."
        }), 504

    except APIError as error:
        current_app.logger.exception("AI provider returned an API error.")

        return jsonify({
            "error": "The AI provider could not complete the request.",
            "details": str(error)
        }), 502

    except RuntimeError as error:
        current_app.logger.exception("AI configuration error.")

        return jsonify({
            "error": str(error)
        }), 503

    except Exception:
        current_app.logger.exception("Unexpected AI analysis error.")

        return jsonify({
            "error": "An unexpected server error occurred during AI analysis."
        }), 500


@main.route("/api/incidents", methods=["GET"])
def incidents():
    recorded_incidents = get_incidents()

    return jsonify({
        "total_incidents": len(recorded_incidents),
        "incidents": recorded_incidents
    })
