# Job Search Platform for People with Disabilities

A full-stack, accessibility-focused job platform built with Streamlit (frontend), Flask (API), and PostgreSQL (database).

## Features

- Accessible job search with accommodation-focused listings
- Company onboarding and verification workflow
- User profile and application tracking
- Resume builder with PDF export (ReportLab)
- REST API for jobs, companies, and applications

## Tech Stack

- Frontend: Streamlit
- Backend API: Flask, Flask-CORS, Flask-Caching
- ORM/Database: SQLAlchemy + PostgreSQL
- Utilities: python-dotenv, ReportLab, Werkzeug

## Project Structure

```text
.
├── Home.py                 # Streamlit entrypoint
├── api/
│   └── app.py              # Flask API entrypoint
├── pages/                  # Streamlit multipage app
├── utils/                  # Database models and data utilities
├── assets/                 # Resume template helpers
├── tests/                  # Smoke and contract tests
├── requirements.txt
└── .env.example
```

## Prerequisites

- Python 3.10+
- PostgreSQL 13+
- PowerShell (for the commands below on Windows)

## Quick Start (Windows / PowerShell)

1. Clone and enter the repository.

```powershell
git clone https://github.com/parth-shinge/Job-search-platform-for-people-with-disabilities.git
cd "Job-search-platform-for-people-with-disabilities"
```

2. Create and activate a virtual environment.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies.

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Configure environment variables.

```powershell
Copy-Item .env.example .env
```

Update `.env` with your local PostgreSQL credentials.

5. Create the database (if needed).

```powershell
psql -U postgres -h localhost -c "CREATE DATABASE mydatabase;"
```

6. Initialize database tables.

```powershell
python .\utils\models.py
```

7. Start the API (Terminal 1).

```powershell
python .\api\app.py
```

8. Start the Streamlit app (Terminal 2).

```powershell
streamlit run .\Home.py
```

## Default Local URLs

- Frontend: http://localhost:8501
- API health: http://localhost:5001/

## API Endpoints (v1)

- `GET /api/v1/jobs`
- `GET /api/v1/companies`
- `GET /api/v1/companies/<company_id>/jobs`
- `POST /api/v1/applications`
- `GET /api/v1/applications/<user_id>`

## Environment Variables

Required:

- `DATABASE_URL` (PostgreSQL connection string)

Optional:

- `FLASK_PORT` (default: `5001`)

## Development Notes

- Install developer tools with:

```powershell
pip install -r requirements.txt
```

- Keep `.env` out of version control. A template is provided in `.env.example`.

## Testing and Verification

Run the following from the project root:

```powershell
pytest -q
python -m compileall api pages utils
```

If both commands complete without errors and the health endpoint returns `200`, the app setup is valid.
