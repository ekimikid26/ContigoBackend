from fastapi import APIRouter, Depends
from supabase import Client
from database import get_supabase
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/notas", tags=["notas"])

@router.post("")
def create_note(data: dict, current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    note = {
        "especialista_id": current_user["id"],
        "paciente_id": data["paciente_id"],
        "texto": data["texto"]
    }
    response = supabase.table("notas_especialista").insert(note).execute()
    return response.data[0]

@router.get("/patient/{patient_id}")
def get_notes(patient_id: int, current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    response = supabase.table("notas_especialista")\
        .select("*")\
        .eq("paciente_id", patient_id)\
        .eq("especialista_id", current_user["id"])\
        .order("created_at", desc=True)\
        .execute()
    return response.data
