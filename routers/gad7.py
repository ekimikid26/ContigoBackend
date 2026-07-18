from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from database import get_supabase
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/gad7", tags=["GAD-7"])

@router.post("")
def save_gad7_result(
    result: dict,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    data = {**result, "user_id": current_user["id"]}
    response = supabase.table("gad7_results").insert(data).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Error saving GAD-7 result")
    return response.data[0]

@router.get("/me")
def get_my_gad7_results(
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    response = supabase.table("gad7_results")\
        .select("*")\
        .eq("user_id", current_user["id"])\
        .order("applied_at", desc=True)\
        .execute()
    return response.data

@router.get("/patient/{patient_id}")
def get_patient_gad7(
    patient_id: int,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    if current_user["rol"] not in ["especialista", "administrador"]:
        raise HTTPException(status_code=403, detail="Sin permisos")
    
    response = supabase.table("gad7_results")\
        .select("*")\
        .eq("user_id", patient_id)\
        .order("applied_at", desc=True)\
        .execute()
    return response.data
