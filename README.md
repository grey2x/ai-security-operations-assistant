# AI Security Operations Assistant

An AI-assisted security monitoring and incident analysis application built with Python and Flask. The application processes authentication logs, identifies suspicious activity using rule-based detection, records security incidents, and provides an interface for AI-assisted incident analysis.

## Project Overview

The goal of this project is to demonstrate how traditional security monitoring and AI-assisted analysis can work together in a lightweight Security Operations Centre (SOC) environment.

### Features

- **Security log ingestion:** Reads and processes structured authentication event logs.
- **Rule-based detection:** Identifies suspicious authentication patterns using transparent detection rules.
- **Incident management:** Stores detected incidents in an SQLite database.
- **Duplicate prevention:** Prevents the same incident from being repeatedly recorded.
- **Dashboard:** Displays security events, alerts, and recorded incidents.
- **AI-assisted analysis:** Integrates with an external AI API to explain security alerts and suggest defensive investigation steps.
- **Error handling:** Handles invalid input, backend failures, and AI provider errors.

## Detection Logic

The current detection engine includes:

| Rule ID | Detection | Severity |
|---|---|---|
| AUTH-001 | Repeated failed login attempts | High |

AUTH-001 identifies five or more failed authentication attempts from the same source IP address within a five-minute window.

The application uses synthetic authentication logs for testing and demonstration.

## Technology Stack

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- OpenAI Python SDK (Gemini-compatible API integration)
- pytest

## Project Structure

```text
ai-security-operations/
├── app/
│   ├── services/
│   │   ├── ai_analyzer.py
│   │   ├── analysis_service.py
│   │   ├── database.py
│   │   ├── detection_engine.py
│   │   └── log_parser.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   ├── __init__.py
│   └── routes.py
├── data/
│   └── samples/
├── reports/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/grey2x/ai-security-operations-assistant.git
cd ai-security-operations-assistant
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root if you want to configure AI analysis.

Add your provider configuration:

```env
AI_PROVIDER=gemini
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=your_supported_model
```

Keep API keys private. Never commit your `.env` file to GitHub.

The core log processing, detection, database, and dashboard functionality does not require an AI API key.

### 5. Run the application

```bash
python run.py
```

Open the dashboard:

http://127.0.0.1:5000

Health endpoint:

http://127.0.0.1:5000/health

## API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Checks backend availability |
| `/api/analyse-samples` | GET | Processes sample authentication logs and records detected incidents |
| `/api/incidents` | GET | Retrieves recorded incidents |
| `/api/ai-analysis` | POST | Requests AI-assisted analysis of an incident |

## Testing

Run the automated test suite:

```bash
python -m pytest -v
```

The current test suite contains 12 passing tests covering application functionality, log processing, detection logic, and AI integration using mocked responses.

Live AI provider connectivity is still being verified separately.

## Security Considerations

- Uses synthetic authentication events for demonstrations.
- Keeps API keys and sensitive configuration outside the source code.
- Uses parameterised SQL queries for database operations.
- Uses safe DOM text insertion when displaying incident information.
- Validates incoming API data before processing.
- Does not automatically classify an alert as a confirmed compromise.

## Current Development Status

- Phase 1: Flask application foundation — Complete.
- Phase 2: Security log ingestion and detection engine — Complete.
- Phase 3: AI-powered incident analysis — Integration implemented; live provider verification outstanding.
- Phase 4: Dashboard and database — Core functionality implemented and tested.
- Phase 5: Final testing, documentation and demonstration — In progress.

## Future Improvements

- Expand detection rules to cover additional authentication and security events.
- Support additional log formats.
- Improve incident reporting and export functionality.
- Add more AI providers and improve provider failure handling.
- Introduce additional defensive investigation workflows.

---

**Disclaimer:** This project is an educational security monitoring application. It uses synthetic data and is not intended to replace a production SIEM or enterprise security monitoring platform.
