from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users, biometrics, emotional_states, activities, alerts, vinculaciones, notas, calibration, payments
from database import get_supabase

app = FastAPI(title="Contigo API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(biometrics.router)
app.include_router(emotional_states.router)
app.include_router(activities.router)
app.include_router(alerts.router)
app.include_router(vinculaciones.router)
app.include_router(notas.router)
app.include_router(calibration.router)
app.include_router(payments.router)

@app.get("/")
async def root():
    return {"message": "Contigo API esta corriendo"}

@app.get("/ping")
def ping():
    return {
        "status": "ok",
        "message": "Backend Contigo funcionando correctamente",
        "version": "1.0.0"
    }

@app.get("/health")
def health(supabase = Depends(get_supabase)):
    try:
        # Verificar si podemos leer la tabla users
        result = supabase.table("users").select("id").limit(1).execute()
        return {
            "status": "ok",
            "database": "conectada",
            "users_table": "accesible"
        }
    except Exception as e:
        return {
            "status": "error",
            "database": "no conectada",
            "detail": str(e)
        }
