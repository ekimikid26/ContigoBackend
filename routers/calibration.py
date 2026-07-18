from fastapi import APIRouter, Depends
from supabase import Client
from database import get_supabase
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/calibration", tags=["calibration"])

@router.get("/status")
def get_calibration_status(current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    status = supabase.table("calibration_data").select("*").eq("user_id", current_user["id"]).execute()
    if not status.data:
        return {"calibration_completed": False, "baseline": None}
    return status.data[0]

@router.post("/data")
def save_calibration_data(data: dict, current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    # Upsert logic for Supabase
    item = {**data, "user_id": current_user["id"]}
    response = supabase.table("calibration_data").upsert(item).execute()
    return response.data[0]

@router.put("/complete")
def complete_calibration(current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    response = supabase.table("calibration_data")\
        .update({"calibration_completed": True})\
        .eq("user_id", current_user["id"])\
        .execute()
    return response.data[0]
