from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from database import get_supabase
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/vinculaciones", tags=["vinculaciones"])

@router.post("/invitation")
def create_invitation(data: dict, current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    if current_user["rol"] != "especialista":
        raise HTTPException(status_code=403, detail="Only specialists can invite")
    
    # Get patient by email
    patient = supabase.table("users").select("*").eq("correo", data["email"]).execute()
    if not patient.data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    invitation = {
        "especialista_id": current_user["id"],
        "paciente_id": patient.data[0]["id"],
        "activa": True
    }
    response = supabase.table("vinculaciones").insert(invitation).execute()
    return response.data[0]

@router.get("/all")
def get_all_vinculaciones(current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    if current_user["rol"] != "administrador":
        raise HTTPException(status_code=403, detail="Only admins can view all linkages")
    response = supabase.table("vinculaciones").select("*").execute()
    return response.data

@router.post("/vincular")
def admin_vincular(data: dict, current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    if current_user["rol"] != "administrador":
        raise HTTPException(status_code=403, detail="Only admins can link")

    # Get IDs from UIDs
    p = supabase.table("users").select("id").eq("uid", data["paciente_uid"]).execute()
    e = supabase.table("users").select("id").eq("uid", data["especialista_uid"]).execute()

    if not p.data or not e.data:
        raise HTTPException(status_code=404, detail="User not found")

    vinculation = {
        "especialista_id": e.data[0]["id"],
        "paciente_id": p.data[0]["id"],
        "activa": True,
        "consentimiento_dado": False
    }
    response = supabase.table("vinculaciones").insert(vinculation).execute()
    return response.data[0]

@router.delete("/{vinculacionId}")
def delete_vinculacion(vinculacionId: int, current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    if current_user["rol"] not in ["administrador", "especialista"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    supabase.table("vinculaciones").delete().eq("id", vinculacionId).execute()
    return {"message": "Vinculación eliminada"}

@router.put("/consent")
def update_consent(data: dict, current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    response = supabase.table("vinculaciones")\
        .update({"consentimiento_dado": data["enabled"]})\
        .eq("paciente_id", current_user["id"])\
        .execute()
    return response.data
