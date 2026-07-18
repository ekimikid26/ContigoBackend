from fastapi import APIRouter, Depends
from supabase import Client
from database import get_supabase
from middleware.auth_middleware import get_current_user
from schemas.activity_log import ActivityLogCreate

router = APIRouter(prefix="/activities", tags=["activities"])

@router.post("")
def log_activity(data: ActivityLogCreate, current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    log = {
        "user_id": current_user["id"],
        "activity_type": data.activity_type,
        "duration_seconds": data.duration_seconds
    }
    response = supabase.table("activity_logs").insert(log).execute()
    return response.data[0]

@router.get("/me")
def get_my_logs(current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    response = supabase.table("activity_logs")\
        .select("*")\
        .eq("user_id", current_user["id"])\
        .order("completed_at", desc=True)\
        .execute()
    return response.data
