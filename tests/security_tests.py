import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_access_notes_without_auth():
    """Prueba que no se puede acceder a notas sin token."""
    response = client.get("/notas/patient/1")
    assert response.status_code == 401

def test_create_note_invalid_role():
    """Simula un usuario con rol 'paciente' intentando crear una nota."""
    # Nota: En una prueba real se necesitaría un token JWT válido con rol paciente
    # Aquí probamos la estructura del endpoint
    response = client.post("/notas", json={"paciente_id": 1, "texto": "Test"})
    assert response.status_code == 401 # Sin auth, falla antes del rol

def test_payment_plans_public_access():
    """Los planes deben ser públicos."""
    response = client.get("/payments/plans")
    assert response.status_code == 200

# Más pruebas requerirían mocks de la base de datos Supabase y tokens JWT válidos
