from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime
from models.user import UserRole

class UserBase(BaseModel):
    nombre: str
    correo: EmailStr
    rol: UserRole

class LoginRequest(BaseModel):
    correo: EmailStr
    password: str

class UserCreate(UserBase):
    password: str
    edad: Optional[int] = None
    sexo: Optional[str] = None
    emergencia_nombre: Optional[str] = None
    emergencia_tel: Optional[str] = None
    medicamentos: Optional[str] = None
    alergias: Optional[str] = None
    plan_tratamiento: Optional[str] = None
    cedula_profesional: Optional[str] = None
    institucion_licenciatura: Optional[str] = None
    cedula_especialidad: Optional[str] = None
    tipo_especialidad: Optional[str] = None
    anios_experiencia: Optional[int] = None
    institucion: Optional[str] = None
    enfoque_terapeutico: Optional[str] = None
    telefono: Optional[str] = None
    historial_medico: Optional[str] = None

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    edad: Optional[int] = None
    # Add other fields as needed

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class ForgotPasswordRequest(BaseModel):
    correo: EmailStr

class UserResponse(UserBase):
    id: int
    uid: str
    activo: bool
    fecha_registro: datetime
    ultimo_acceso: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    user_id: int
    uid: str
    rol: str
