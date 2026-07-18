from passlib.context import CryptContext
import bcrypt

# Configuración de passlib para compatibilidad general
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # Primero intentar con bcrypt directo (más robusto en Windows)
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        # Fallback a passlib por si el hash tiene formato antiguo
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False

def get_password_hash(password: str) -> str:
    # Usar bcrypt directo para asegurar hashes perfectos de 60 caracteres
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
