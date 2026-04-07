from fastapi import FastAPI

from app.api.v1.projects import router as projects_router
from app.api.v1.runs import router as runs_router

app = FastAPI(title="AI Growth Audit API", version="0.1.0")


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(projects_router)
app.include_router(runs_router)
