import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Solo cargamos el .env si estamos en local
if os.path.exists(".env"):
    load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ERROR: Faltan llaves de Supabase")
    supabase = None
else:
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Cliente de Supabase conectado")
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        supabase = None

def get_supabase() -> Client:
    return supabase