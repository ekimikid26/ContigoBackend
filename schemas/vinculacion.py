from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from schemas.user import UserResponse

class VinculacionBase(BaseModel):
    paciente_id: int
    especialista_id: int

class VinculacionCreate(VinculacionBase):
    pass

class VinculacionResponse(VinculacionBase):
    id: int
    fecha_vinculacion: datetime
    activa: bool
    consentimiento_dado: bool
    paciente: Optional[UserResponse] = None
    especialista: Optional[UserResponse] = None

    class Config:
        from_attributes = True

class ConsentUpdate(BaseModel):
    consentimiento_dado: bool
