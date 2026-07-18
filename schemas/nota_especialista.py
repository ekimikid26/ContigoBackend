from pydantic import BaseModel
from datetime import datetime

class NotaEspecialistaBase(BaseModel):
    paciente_id: int
    texto: str

class NotaEspecialistaCreate(NotaEspecialistaBase):
    pass

class NotaEspecialistaResponse(NotaEspecialistaBase):
    id: int
    especialista_id: int
    created_at: datetime

    class Config:
        from_attributes = True
