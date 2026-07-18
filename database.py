import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Forzar la carga del archivo .env buscando en el directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, ".env")
load_dotenv(dotenv_path=dotenv_path, override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "SUPABASE_URL y SUPABASE_SERVICE_KEY deben estar "
        "configurados en el archivo .env"
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase() -> Client:
    return supabase
