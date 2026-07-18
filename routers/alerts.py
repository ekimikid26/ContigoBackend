from fastapi import APIRouter, Depends
from supabase import Client
from database import get_supabase
from middleware.auth_middleware import get_current_user
from schemas.alert import AlertCreate

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.post("")
def create_alert(data: AlertCreate, current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    alert = {
        "user_id": current_user["id"],
        "risk_level": data.risk_level
    }
    response = supabase.table("alerts").insert(alert).execute()
    return response.data[0]

@router.get("/me")
def get_my_alerts(current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    response = supabase.table("alerts")\
        .select("*")\
        .eq("user_id", current_user["id"])\
        .order("generated_at", desc=True)\
        .execute()
    return response.data
