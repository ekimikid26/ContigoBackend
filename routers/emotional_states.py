from fastapi import APIRouter, Depends
from supabase import Client
from database import get_supabase
from middleware.auth_middleware import get_current_user
from schemas.emotional_state import EmotionalStateCreate

router = APIRouter(prefix="/emotional-states", tags=["emotions"])

@router.post("")
def save_emotion(data: EmotionalStateCreate, current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    item = {"user_id": current_user["id"], "emotional_state": data.emotional_state}
    response = supabase.table("emotional_states").insert(item).execute()
    return response.data[0]

@router.get("/recent")
def get_recent_emotions(current_user: dict = Depends(get_current_user), supabase: Client = Depends(get_supabase)):
    response = supabase.table("emotional_states")\
        .select("*")\
        .eq("user_id", current_user["id"])\
        .order("registered_at", desc=True)\
        .limit(10)\
        .execute()
    return response.data
