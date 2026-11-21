# CRUS Architecture

## Phase 1 components

- FastAPI application and REST API
- SQLAlchemy models
- SQLite demo database
- PostgreSQL production-oriented database
- Redis infrastructure
- Docker Compose deployment
- Windows PowerShell scripts
- Health and dashboard endpoints

## Core entities

- **Agent:** role, status, model, demo flag and execution state
- **Project:** isolated workspace metadata and progress state
- **Task:** project relation, priority, status, dependencies and retry state

## Persistence

The default demo uses SQLite. PostgreSQL is configured through Docker Compose. Both databases use the same SQLAlchemy models.
