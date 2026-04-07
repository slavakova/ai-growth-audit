# AI Growth Audit — MVP Backend + Frontend

## Backend stack
- Python 3.12
- FastAPI
- SQLAlchemy 2.0
- Alembic
- PostgreSQL
- Redis
- Celery
- Pydantic v2
- Docker Compose

## Backend run

```bash
cp .env.example .env
docker compose up --build
```

API: `http://localhost:8000`

## Backend migrations

```bash
docker compose run --rm api alembic upgrade head
```

## Backend tests

```bash
docker compose run --rm api pytest
```

## Frontend MVP (Next.js + TypeScript + Tailwind)

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

App: `http://localhost:3000`

By default frontend uses mock API responses (`NEXT_PUBLIC_USE_MOCK=true`).

## Frontend screens

- `/projects` — projects list
- `/projects/new` — project creation
- `/runs/[id]` — run summary
- `/runs/[id]/competitors` — competitors
- `/runs/[id]/comparison` — comparison metrics
- `/runs/[id]/recommendations` — recommendations
- `/runs/[id]/assets` — generated assets

## Notes

- Crawler v1 is HTTP-only (no browser automation): loads HTML and extracts structured fields.
- Pipeline remains scaffolded for future real SERP/LLM integrations.
