from app.models.enums import AnalysisGoal


def test_projects_crud_flow(client):
    payload = {
        "name": "My project",
        "website_url": "https://example.com",
        "region": "US",
        "priority_service": "SEO audit",
    }
    created = client.post("/api/projects", json=payload)
    assert created.status_code == 201
    project_id = created.json()["id"]

    listed = client.get("/api/projects")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    fetched = client.get(f"/api/projects/{project_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == payload["name"]

    run = client.post(f"/api/projects/{project_id}/analyze", json={"goal": AnalysisGoal.SEO_GROWTH.value})
    assert run.status_code == 202
    assert run.json()["project_id"] == project_id
