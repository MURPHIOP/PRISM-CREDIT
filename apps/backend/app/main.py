from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.risk import router as risk_router
from app.ml.predictor import RiskEngine
from app.ml.audit_logger import AuditLogger

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.risk_engine = RiskEngine()
    app.state.audit_logger = AuditLogger()
    yield

app = FastAPI(
    title="PRISM Credit Risk API",
    description="Behavioral AI-driven credit risk evaluation system with explainable and compliance-aware architecture.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(risk_router, prefix="/api/v1")

@app.get("/")
async def health_check():
    return {
        "status": "healthy",
        "service": "PRISM Credit Risk API",
        "version": "1.0.0"
    }