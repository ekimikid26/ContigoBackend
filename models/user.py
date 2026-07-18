import enum

class UserRole(str, enum.Enum):
    paciente = "paciente"
    especialista = "especialista"
    administrador = "administrador"

class User:
    # Esta clase ahora es solo referencial ya que Supabase
    # maneja el esquema directamente en la base de datos.
    pass
