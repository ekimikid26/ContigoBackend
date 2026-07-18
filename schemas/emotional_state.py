from pydantic import BaseModel
from datetime import datetime

class EmotionalStateBase(BaseModel):
    emotional_state: str

class EmotionalStateCreate(EmotionalStateBase):
    pass

class EmotionalStateResponse(EmotionalStateBase):
    id: int
    user_id: int
    registered_at: datetime

    class Config:
        from_attributes = True
