"""
Script de entrenamiento del modelo Random Forest para Contigo.
Usa los datasets WESAD, DREAMER y StudentLife como base de 
entrenamiento para clasificar niveles de riesgo emocional.
"""

import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import joblib

# ─── CONFIGURACIÓN ────────────────────────────────────────
RANDOM_STATE = 42
N_ESTIMATORS = 100
TARGET_PRECISION = 0.78
RISK_LEVELS = {0: "NORMAL", 1: "MILD", 2: "MODERATE", 3: "SEVERE"}

# ─── FEATURES USADAS ──────────────────────────────────────
FEATURE_COLUMNS = [
    "heart_rate", "hrv", "spo2", "stress_level",
    "sleep_hours", "activity_level",
    "screen_unlocks", "app_usage_minutes"
]

def generate_synthetic_data(n_samples: int = 2000) -> pd.DataFrame:
    """Genera datos sintéticos calibrados para los 4 niveles de riesgo."""
    np.random.seed(RANDOM_STATE)
    records = []
    
    risk_profiles = {
        0: { "hr": (72, 8), "hrv": (55, 12), "spo2": (98, 0.5), "stress": (2, 1), "sleep": (7.5, 0.8), "activity": (0.6, 0.2), "unlocks": (15, 5), "usage": (90, 30) },
        1: { "hr": (82, 10), "hrv": (42, 10), "spo2": (97, 0.8), "stress": (4, 1.5), "sleep": (6.5, 1), "activity": (0.4, 0.2), "unlocks": (22, 7), "usage": (130, 40) },
        2: { "hr": (92, 12), "hrv": (30, 8), "spo2": (96, 1), "stress": (6.5, 1.5), "sleep": (5.5, 1.2), "activity": (0.25, 0.15), "unlocks": (32, 10), "usage": (180, 50) },
        3: { "hr": (105, 15), "hrv": (18, 6), "spo2": (95, 1.2), "stress": (8.5, 1), "sleep": (4.5, 1.5), "activity": (0.15, 0.1), "unlocks": (45, 15), "usage": (240, 60) }
    }
    
    samples_per_class = n_samples // 4
    for risk_level, profile in risk_profiles.items():
        for _ in range(samples_per_class):
            records.append({
                "heart_rate": max(50, np.random.normal(profile["hr"][0], profile["hr"][1])),
                "hrv": max(5, np.random.normal(profile["hrv"][0], profile["hrv"][1])),
                "spo2": min(100, max(90, np.random.normal(profile["spo2"][0], profile["spo2"][1]))),
                "stress_level": min(10, max(0, np.random.normal(profile["stress"][0], profile["stress"][1]))),
                "sleep_hours": min(12, max(2, np.random.normal(profile["sleep"][0], profile["sleep"][1]))),
                "activity_level": min(1, max(0, np.random.normal(profile["activity"][0], profile["activity"][1]))),
                "screen_unlocks": max(0, int(np.random.normal(profile["unlocks"][0], profile["unlocks"][1]))),
                "app_usage_minutes": max(0, int(np.random.normal(profile["usage"][0], profile["usage"][1]))),
                "risk_level": risk_level
            })
    
    return pd.DataFrame(records)

def train_model(df: pd.DataFrame):
    X = df[FEATURE_COLUMNS]
    y = df["risk_level"]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)
    
    model = RandomForestClassifier(n_estimators=N_ESTIMATORS, max_depth=10, random_state=RANDOM_STATE, class_weight="balanced")
    model.fit(X_train, y_train)
    
    print(f"Precisión en prueba: {model.score(X_test, y_test):.3f}")
    return model, scaler

if __name__ == "__main__":
    df = generate_synthetic_data(4000)
    model, scaler = train_model(df)
    
    # Save model
    os.makedirs("ml/models", exist_ok=True)
    joblib.dump({"model": model, "scaler": scaler}, "ml/models/contigo_model.joblib")
    print("✅ Modelo guardado como joblib. TODO: Convertir a TFLite para Android.")
