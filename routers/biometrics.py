from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from database import get_supabase
from middleware.auth_middleware import get_current_user
from typing import List

router = APIRouter(prefix="/biometrics", tags=["biometrics"])

@router.post("")
def save_biometric(reading: dict, current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    data = {**reading, "user_id": current_user["id"]}
    response = supabase.table("biometric_readings").insert(data).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Error saving reading")
    return response.data[0]

@router.get("/me")
def get_my_biometrics(days: int = 7, current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    response = supabase.table("biometric_readings")\
        .select("*")\
        .eq("user_id", current_user["id"])\
        .order("timestamp", desc=True)\
        .limit(days * 24)\
        .execute()
    return response.data
