# CRUS API Dokümantasyonu

Swagger: `http://127.0.0.1:8000/docs`

## Health

`GET /api/health`

## Dashboard

`GET /api/dashboard`

## Agents

- `GET /api/agents`
- `GET /api/agents/{agent_id}`
- `POST /api/agents/{agent_id}/{action}`

## Projects

- `GET /api/projects`
- `POST /api/projects`
- `GET /api/projects/{project_id}`
- `PATCH /api/projects/{project_id}`
- `POST /api/projects/{project_id}/action/{action}`

## Tasks

- `GET /api/tasks`
- `POST /api/projects/{project_id}/tasks`
- `PATCH /api/tasks/{task_id}`
