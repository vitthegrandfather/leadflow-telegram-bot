# LeadFlow Bot

A Telegram lead-intake bot with a lightweight CRM workflow for a small service studio.

**This is a personal portfolio demonstration project.** It is not paid client work, not a production SaaS, and not affiliated with a live agency. The code is intentionally complete enough to demonstrate production-minded structure, tests, and documentation.

Customers submit a structured brief in Telegram. Administrators receive a notification, inspect the request, change status, add an internal note, view counts, and export leads to CSV.

Curated portfolio screenshots from an interactive workflow walkthrough are included in
`portfolio/`. The Python bot remains the implementation artifact.

## Interactive showcase

The `showcase/` directory contains the browser walkthrough used in the portfolio. It mirrors
the same lead lifecycle with fictional data and never connects to Telegram or a live CRM.

```bash
cd showcase
npm ci
npm run dev
```

The showcase is intentionally separate from the Python runtime: reviewers can explore the
workflow without a bot token, while the production-minded implementation remains in `app/`.

## Features

- Customer `/start` menu: submit a request, view personal requests, about
- Finite-state intake form: name, phone, service category, description, contact method
- Confirmation with confirm / edit / cancel
- Human-readable lead numbers (`LF-YYMMDD-XXXX`)
- Administrator `/admin` desk with counts, pagination, status changes, notes, CSV export
- Customer notification when public status changes
- Administrator access restricted by Telegram user IDs
- Duplicate-submission protection (same user + phone + category + description within 10 minutes)
- Input validation, phone normalisation, HTML escaping
- Structured JSON logging and a central error handler
- SQLite + Alembic migrations
- Docker Compose
- Automated tests that never call Telegram

## Architecture

Handlers stay thin. Services own business rules. Repositories own SQL.

```text
Telegram update
    → middlewares (logging, DB session, admin callback guard)
    → handlers (customer / admin)
    → services (lead, auth, validation, export, notifications)
    → repositories (SQLAlchemy)
    → SQLite
```

## Technology stack

| Layer | Choice |
| --- | --- |
| Runtime | Python 3.12 (3.10+ supported) |
| Bot | aiogram 3 |
| ORM | SQLAlchemy 2 (async) |
| Database | SQLite via aiosqlite |
| Migrations | Alembic |
| Settings | Pydantic Settings |
| Tests | pytest, pytest-asyncio |
| Lint | Ruff |
| Containers | Docker, Docker Compose |

## Local setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Create a bot token with [@BotFather](https://t.me/BotFather) and put it in `.env` as `BOT_TOKEN`. Add your Telegram user ID to `ADMIN_IDS`.

```bash
alembic upgrade head
python -m app.seed
python -m app.main
```

`python -m app.main` starts long polling. The process must be able to reach `api.telegram.org`.

## Environment variables

| Variable | Required | Description |
| --- | --- | --- |
| `BOT_TOKEN` | yes to run the bot | Token from BotFather |
| `ADMIN_IDS` | yes for admin access | Comma-separated Telegram user IDs |
| `DATABASE_URL` | no | Default `sqlite+aiosqlite:///./data/leadflow.db` |
| `LOG_LEVEL` | no | Default `INFO` |

Copy `.env.example`. Never commit `.env`.

## Database migrations

```bash
alembic upgrade head
alembic revision --autogenerate -m "describe change"
```

The bot also applies `alembic upgrade head` on startup. Sample data:

```bash
python -m app.seed
```

The seed script inserts fictional leads across every status and does nothing if eight or more leads already exist.

## Tests and lint

```bash
pytest
ruff check .
ruff format --check .
```

Tests use an in-memory SQLite database and mock Telegram API calls. They do not require `BOT_TOKEN`.
GitHub Actions runs the same checks on Python 3.10, 3.11, and 3.12.

## Docker

```bash
cp .env.example .env
docker compose up --build
```

SQLite lives in the `leadflow-data` volume. The image uses Python 3.12.

## Project structure

```text
app/
  main.py              entrypoint
  config.py            environment settings
  bot.py               dispatcher wiring
  handlers/            Telegram adapters
  keyboards/           inline keyboards
  states/              FSM groups
  services/            business logic
  repositories/        database access
  models/              Lead + enums
  database/            engine, sessions
  middlewares/         db, auth, logging
  utils/               public IDs, HTML formatting
  seed.py              fictional demo leads
alembic/               migrations
tests/                 pytest suite
```

## Security notes

- Administrator commands and `a:` callbacks are authorised against `ADMIN_IDS`
- User-provided strings are HTML-escaped before being sent back to Telegram
- Phone numbers are normalised to a `+` plus digits form
- Duplicate briefs from the same user are rejected inside a short window
- Tokens and secrets belong in environment variables, never in source control
- This demo uses SQLite and long polling; it is not hardened for a public multi-tenant deployment

## Demo limitations

- Long polling, not a webhook
- In-memory FSM (form state does not survive process restart)
- SQLite is the demonstration database
- No billing, no file attachments, no multi-tenant organisations
- Sample names and numbers are fictional
- The interactive web showcase shares the lead model for walkthroughs; the Python bot is the portfolio artifact

See [DEMO.md](DEMO.md) for a screenshot sequence, BotFather steps, and portfolio captions.
See [PORTFOLIO.md](PORTFOLIO.md) for a ready-to-use Upwork case description.
