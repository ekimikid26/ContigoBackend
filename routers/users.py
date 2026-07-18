from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from database import get_supabase
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    return current_user

@router.put("/me")
def update_me(updates: dict, current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    response = supabase.table("users").update(updates).eq("id", current_user["id"]).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Error updating user")
    return response.data[0]

@router.get("/all")
def get_all_users(
    rol: str = None,
    search: str = None,
    page: int = 1,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    if current_user["rol"] != "administrador":
        raise HTTPException(status_code=403, detail="Only admins can view all users")

    query = supabase.table("users").select("*")

    if rol:
        query = query.eq("rol", rol)
    if search:
        query = query.ilike("nombre", f"%{search}%")

    # Paginación
    start = (page - 1) * limit
    end = start + limit - 1

    response = query.range(start, end).order("fecha_registro", desc=True).execute()
    return response.data

@router.put("/{uid}/admin-update")
def admin_update_user(
    uid: str,
    body: dict,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    if current_user["rol"] != "administrador":
        raise HTTPException(status_code=403,
                           detail="Solo administradores")
    supabase.table("users")\
        .update({
            "nombre": body.get("nombre"),
            "correo": body.get("correo"),
            "rol": body.get("rol"),
            "activo": body.get("activo")
        })\
        .eq("uid", uid)\
        .execute()
    return {"message": "Usuario actualizado"}

@router.get("/patients")
def get_my_patients(current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    if current_user["rol"] != "especialista":
        raise HTTPException(status_code=403, detail="Only specialists can view patients")
    
    # Get vinculaciones
    vinculaciones = supabase.table("vinculaciones")\
        .select("paciente_id")\
        .eq("especialista_id", current_user["id"])\
        .eq("activa", True).execute()
    
    patient_ids = [v["paciente_id"] for v in vinculaciones.data]
    if not patient_ids:
        return []
    
    patients = supabase.table("users").select("*").in_("id", patient_ids).execute()
    return patients.data
