# AI Security Operations Assistant

An AI-assisted security monitoring and incident analysis application.

## Project goals

- Ingest and process security logs.
- Identify suspicious patterns using transparent detection rules.
- Use an AI model to help explain findings.
- Maintain incident history.
- Generate incident reports and defensive recommendations.

## Technology

- Python and Flask
- HTML, CSS and JavaScript
- SQLite (planned)
- AI API integration (planned)
- pytest

## Current stage

Phase 1 — application foundation.

## Setup

Create and activate a virtual environment:

### Windows PowerShell
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest -v
```

Start the development server:

```bash
python run.py
```

Open http://127.0.0.1:5000 in your browser.

Health endpoint: http://127.0.0.1:5000/health

## Security note

Do not commit `.env` files, API keys, credentials, or real sensitive logs.
Use synthetic or appropriately sanitised logs for development and demonstrations.
