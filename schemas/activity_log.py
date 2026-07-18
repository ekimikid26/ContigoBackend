from pydantic import BaseModel
from datetime import datetime

class ActivityLogBase(BaseModel):
    activity_type: str
    duration_seconds: int

class ActivityLogCreate(ActivityLogBase):
    pass

class ActivityLogResponse(ActivityLogBase):
    id: int
    user_id: int
    completed_at: datetime

    class Config:
        from_attributes = True
