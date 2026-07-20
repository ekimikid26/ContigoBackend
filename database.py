import os
from supabase import create_client, Client
from dotenv import load_dotenv

# En producción (Railway), las variables ya están en el sistema.
# load_dotenv solo es necesario para desarrollo local.
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Si faltan las variables, lanzamos un error claro que verás en los logs
if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ERROR: Faltan SUPABASE_URL o SUPABASE_SERVICE_KEY en las variables de entorno")
    supabase = None
else:
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Cliente de Supabase inicializado correctamente")
    except Exception as e:
        print(f"❌ ERROR al conectar con Supabase: {e}")
        supabase = None

def get_supabase() -> Client:
    if supabase is None:
        raise ValueError("El cliente de Supabase no está configurado.")
    return supabase