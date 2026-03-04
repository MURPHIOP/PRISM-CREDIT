from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from app.ml.predictor import RiskEngine

router = APIRouter()
risk_engine = RiskEngine()

class RiskRequest(BaseModel):
    income: float = Field(..., ge=0)
    expenses: float = Field(..., ge=0)
    savings: float = Field(..., ge=0)
    transaction_count: int = Field(..., ge=0)

class ExplanationModel(BaseModel):
    factor: str
    impact: str
    weight: float
    description: str

class ComplianceModel(BaseModel):
    demographic_data_used: bool
    model_type: str
    explainability: str
    audit_version: str

class RiskResponse(BaseModel):
    score: int
    risk_level: str
    explanations: List[ExplanationModel]
    compliance: ComplianceModel

@router.post("/predict", response_model=RiskResponse)
async def predict_risk(request: RiskRequest):
    try:
        raw_input = request.model_dump()
        result = risk_engine.process(raw_input)
        return result
    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")