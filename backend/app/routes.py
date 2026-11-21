from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Agent, Project, Task, new_id
from app.schemas import ProjectCreate, ProjectUpdate, TaskCreate, TaskUpdate

router = APIRouter(prefix="/api")


@router.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "healthy", "mode": settings.mode, "database": "connected"}


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    agents = db.query(Agent).all()
    tasks = db.query(Task).all()
    return {"total_projects": len(projects), "active_projects": sum(p.status in {"RUNNING", "ACTIVE"} for p in projects), "completed_projects": sum(p.status == "COMPLETED" for p in projects), "active_agents": sum(a.status == "WORKING" for a in agents), "idle_agents": sum(a.status == "IDLE" for a in agents), "failed_tasks": sum(t.status == "FAILED" for t in tasks), "pending_tasks": sum(t.status in {"PENDING", "QUEUED"} for t in tasks), "mode": settings.mode}


@router.get("/agents")
def list_agents(db: Session = Depends(get_db)):
    return db.query(Agent).order_by(Agent.role).all()


@router.get("/agents/{agent_id}")
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(404, "Agent not found")
    return agent


@router.post("/agents/{agent_id}/{action}")
def control_agent(agent_id: str, action: str, db: Session = Depends(get_db)):
    agent = db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(404, "Agent not found")
    allowed = {"start": "IDLE", "pause": "PAUSED", "resume": "IDLE", "stop": "COMPLETED", "restart": "IDLE"}
    if action not in allowed:
        raise HTTPException(400, "Invalid action")
    agent.status = allowed[action]
    db.commit()
    return {"id": agent.id, "status": agent.status, "action": action}


@router.get("/projects")
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.created_at.desc()).all()


@router.post("/projects", status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    project_id = new_id("project")
    project = Project(id=project_id, name=payload.name, description=payload.description, project_type=payload.project_type, requirements=payload.requirements, technologies=payload.technologies, priority=payload.priority, status="PENDING", progress=0, workspace_path=f"workspaces/{project_id}")
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects/{project_id}")
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    agents = db.query(Agent).filter(Agent.current_project_id == project_id).all()
    return {"project": project, "tasks": tasks, "agents": agents}


@router.patch("/projects/{project_id}")
def update_project(project_id: str, payload: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


@router.post("/projects/{project_id}/action/{action}")
def project_action(project_id: str, action: str, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    actions = {"start": "RUNNING", "pause": "PAUSED", "resume": "RUNNING", "cancel": "CANCELLED"}
    if action not in actions:
        raise HTTPException(400, "Invalid action")
    project.status = actions[action]
    db.commit()
    return {"id": project.id, "status": project.status}


@router.get("/tasks")
def list_tasks(project_id: str | None = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(Task)
    if project_id:
        query = query.filter(Task.project_id == project_id)
    return query.order_by(Task.created_at.desc()).all()


@router.post("/projects/{project_id}/tasks", status_code=201)
def create_task(project_id: str, payload: TaskCreate, db: Session = Depends(get_db)):
    if not db.get(Project, project_id):
        raise HTTPException(404, "Project not found")
    task = Task(id=new_id("task"), project_id=project_id, **payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task
