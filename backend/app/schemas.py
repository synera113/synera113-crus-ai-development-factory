from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    description: str = Field(min_length=2)
    project_type: str = "web_application"
    requirements: str = ""
    technologies: str = ""
    priority: str = "MEDIUM"


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=200)
    description: str | None = None
    status: str | None = None
    progress: int | None = Field(default=None, ge=0, le=100)


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str = ""
    priority: str = "MEDIUM"
    agent_role: str | None = None


class TaskUpdate(BaseModel):
    status: str | None = None
    agent_role: str | None = None
    result: str | None = None
