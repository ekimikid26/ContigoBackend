from pydantic import BaseModel
from datetime import datetime
from models.alert import RiskLevel

class AlertBase(BaseModel):
    risk_level: RiskLevel

class AlertCreate(AlertBase):
    pass

class AlertResponse(AlertBase):
    id: int
    user_id: int
    generated_at: datetime
    acknowledged: bool

    class Config:
        from_attributes = True
