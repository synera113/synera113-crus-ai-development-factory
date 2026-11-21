from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine, SessionLocal
from app.models import Agent
from app.routes import router


AGENT_ROLES = [
    ("MASTER", "MASTER", "Proje koordinasyonu, görev dağıtımı ve doğrulama."),
    ("ARCHITECT", "ARCHITECT", "Teknik mimari, tasarım ve bileşen kararları."),
    ("DEVELOPER", "DEVELOPER", "Genel uygulama geliştirme ve entegrasyon."),
    ("FRONTEND", "FRONTEND", "React, UI ve kullanıcı deneyimi geliştirme."),
    ("BACKEND", "BACKEND", "API, iş mantığı ve sunucu uygulaması geliştirme."),
    ("DATABASE", "DATABASE", "Veri modeli, sorgular ve migration yönetimi."),
    ("SECURITY", "SECURITY", "Kimlik, yetkilendirme ve güvenlik denetimi."),
    ("TESTER", "TESTER", "Unit, integration, build ve kalite testleri."),
    ("RESEARCHER", "RESEARCHER", "Teknoloji araştırması ve gereksinim analizi."),
    ("OPTIMIZER", "OPTIMIZER", "Performans, kod kalitesi ve optimizasyon."),
]


def seed_agents(db):
    for role, name, description in AGENT_ROLES:
        if not db.query(Agent).filter(Agent.role == role).first():
            db.add(Agent(id=f"agent-{role.lower()}", name=f"CRUS {name}", role=role, description=description, system_instructions=f"You are the {role} specialist.", status="IDLE", model="demo-simulator" if settings.mode == "demo" else "not-configured", demo=settings.mode == "demo"))
    db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_agents(db)
    finally:
        db.close()
    yield


app = FastAPI(title="CRUS AI Development Factory", version="0.1.0-phase1", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)
