# AI Growth Audit — MVP Backend

MVP backend for analyzing a website, competitors, and growth points.

## Stack
- Python 3.12
- FastAPI
- SQLAlchemy 2.0
- Alembic
- PostgreSQL
- Redis
- Celery
- Pydantic v2
- Docker Compose

## Run with Docker

```bash
cp .env.example .env
docker compose up --build
```

API: `http://localhost:8000`

## Migrations

```bash
docker compose run --rm api alembic upgrade head
```

## Tests

```bash
docker compose run --rm api pytest
```

## Endpoints

- `GET /health`
- `POST /api/projects`
- `GET /api/projects`
- `GET /api/projects/{id}`
- `POST /api/projects/{id}/analyze`
- `GET /api/runs/{id}`
- `GET /api/runs/{id}/competitors`
- `GET /api/runs/{id}/comparison`
- `GET /api/runs/{id}/recommendations`
- `GET /api/runs/{id}/assets/{assetType}`


## Site crawler v1

- HTTP crawler downloads HTML for `selected_page_url` (if set) or project `website_url`.
- Extraction includes: title, meta description, h1, full text, h2/h3, CTA buttons, phones, forms count, messengers, has_price, has_faq, has_reviews, page_type.
- Parsed payload is stored in `site_pages` and `extracted_json`.
- Browser automation is intentionally not used in this version.

## Architecture notes

- Routers only orchestrate request/response and DI.
- Service layer contains business orchestration and stubs.
- DB access is isolated through SQLAlchemy session and model classes.
- Celery pipeline uses scaffolded stages with TODO stubs.

## Where stubs/mocks are used

- `app/services/pipeline_service.py` — all pipeline stages return mock payloads.
- `app/services/run_service.py:finalize_with_mock_data` — writes mock competitors, comparison metric, recommendation and generated asset.
- `app/tasks/pipeline.py` — stage wiring exists; real providers are TODO.

## TODO integration points

1. **Real crawler**
   - Replace `PipelineService.crawl` and `PipelineService.competitor_crawl`.
2. **Real SERP source**
   - Replace `PipelineService.serp_collection` and part of `query_builder` flow.
3. **Real LLM generation**
   - Replace `PipelineService.page_understanding`, `recommendations`, and `generation`.
   - Replace `RunService.finalize_with_mock_data` with real persisted outputs.
