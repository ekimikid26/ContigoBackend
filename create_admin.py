import os
import sys
import getpass
import uuid
from dotenv import load_dotenv
import bcrypt

# Forzar la carga del archivo .env
current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, ".env")
load_dotenv(dotenv_path=dotenv_path, override=True)

def create_admin():
    try:
        from supabase import create_client
    except ImportError:
        print("Error: Instala las dependencias primero: pip install supabase")
        sys.exit(1)

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

    if not supabase_url or not supabase_key:
        print(f"Error: Configura SUPABASE_URL y SUPABASE_SERVICE_KEY en {dotenv_path}")
        sys.exit(1)

    print("\n=== Crear cuenta Administrador de Contigo ===\n")

    correo = input("Correo del administrador: ").strip()
    nombre = input("Nombre del administrador: ").strip()
    password = getpass.getpass("Contraseña (mínimo 8 caracteres): ")

    if len(password) < 8:
        print("Error: La contraseña debe tener al menos 8 caracteres")
        sys.exit(1)

    # Generar hash perfecto con bcrypt
    salt = bcrypt.gensalt(rounds=12)
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    uid = str(uuid.uuid4())
    supabase = create_client(supabase_url, supabase_key)

    try:
        # Verificar si ya existe
        existing = supabase.table("users").select("id").eq("correo", correo).execute()
        if existing.data:
            print(f"\nError: Ya existe un usuario con el correo {correo}")
            choice = input("¿Deseas actualizar su contraseña a la nueva? (s/n): ")
            if choice.lower() == 's':
                supabase.table("users").update({"password_hash": password_hash}).eq("correo", correo).execute()
                print("\n✅ Contraseña actualizada correctamente.")
            sys.exit(0)

        # Crear el administrador
        result = supabase.table("users").insert({
            "uid": uid,
            "nombre": nombre,
            "correo": correo,
            "password_hash": password_hash,
            "rol": "administrador",
            "activo": True
        }).execute()

        if result.data:
            print(f"\n✅ Administrador creado exitosamente")
            print(f"   Correo: {correo}")
            print(f"\nYa puedes iniciar sesión en la app con estas credenciales.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    create_admin()
