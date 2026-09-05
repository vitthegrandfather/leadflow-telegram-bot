FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_URL=sqlite+aiosqlite:///./data/leadflow.db

COPY pyproject.toml README.md alembic.ini ./
COPY app ./app
COPY alembic ./alembic

RUN pip install --no-cache-dir . \
    && mkdir -p /app/data

CMD ["python", "-m", "app.main"]
