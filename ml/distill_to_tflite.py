"""
Destilación de conocimiento: Random Forest (contigo_model.joblib) -> Red neuronal pequeña -> TFLite.

El script original (convert_to_tflite.py) creaba una red con pesos aleatorios SIN
entrenar y nunca usaba el Random Forest cargado. Este script corrige eso: entrena
la red pequeña para imitar las predicciones del Random Forest real, valida el
acuerdo entre ambos modelos, y solo entonces exporta a TFLite.
"""

import os
import json
import numpy as np
import joblib
import tensorflow as tf
from sklearn.metrics import accuracy_score, classification_report

RANDOM_STATE = 42
FEATURE_COLUMNS = [
    "heart_rate", "hrv", "spo2", "stress_level",
    "sleep_hours", "activity_level",
    "screen_unlocks", "app_usage_minutes"
]

MODEL_PATH = os.path.join("ml", "models", "contigo_model.joblib")
TFLITE_PATH = os.path.join("ml", "models", "contigo_model.tflite")
SCALER_JSON_PATH = os.path.join("ml", "models", "scaler_params.json")

def regenerate_synthetic_data(n_samples=4000):
    """Misma generación sintética usada en train_random_forest.py, para tener
    puntos de entrada representativos con los que destilar el conocimiento del RF."""
    np.random.seed(RANDOM_STATE)
    records = []
    risk_profiles = {
        0: {"hr": (72, 8), "hrv": (55, 12), "spo2": (98, 0.5), "stress": (2, 1), "sleep": (7.5, 0.8), "activity": (0.6, 0.2), "unlocks": (15, 5), "usage": (90, 30)},
        1: {"hr": (82, 10), "hrv": (42, 10), "spo2": (97, 0.8), "stress": (4, 1.5), "sleep": (6.5, 1), "activity": (0.4, 0.2), "unlocks": (22, 7), "usage": (130, 40)},
        2: {"hr": (92, 12), "hrv": (30, 8), "spo2": (96, 1), "stress": (6.5, 1.5), "sleep": (5.5, 1.2), "activity": (0.25, 0.15), "unlocks": (32, 10), "usage": (180, 50)},
        3: {"hr": (105, 15), "hrv": (18, 6), "spo2": (95, 1.2), "stress": (8.5, 1), "sleep": (4.5, 1.5), "activity": (0.15, 0.1), "unlocks": (45, 15), "usage": (240, 60)},
    }
    samples_per_class = n_samples // 4
    for risk_level, p in risk_profiles.items():
        for _ in range(samples_per_class):
            records.append([
                max(50, np.random.normal(*p["hr"])),
                max(5, np.random.normal(*p["hrv"])),
                min(100, max(90, np.random.normal(*p["spo2"]))),
                min(10, max(0, np.random.normal(*p["stress"]))),
                min(12, max(2, np.random.normal(*p["sleep"]))),
                min(1, max(0, np.random.normal(*p["activity"]))),
                max(0, int(np.random.normal(*p["unlocks"]))),
                max(0, int(np.random.normal(*p["usage"]))),
            ])
    return np.array(records, dtype=np.float32)

def main():
    print(f"Cargando modelo entrenado desde {MODEL_PATH}...")
    bundle = joblib.load(MODEL_PATH)
    rf_model = bundle["model"]
    scaler = bundle["scaler"]

    print("Regenerando datos representativos para destilación...")
    X_raw = regenerate_synthetic_data(6000)
    X_scaled = scaler.transform(X_raw).astype(np.float32)

    # Etiquetas "blandas" (probabilidades) del Random Forest real: esto es lo
    # que la red pequeña va a aprender a imitar.
    rf_probs = rf_model.predict_proba(X_scaled)
    rf_hard_labels = rf_model.predict(X_scaled)

    split = int(len(X_scaled) * 0.85)
    X_train, X_val = X_scaled[:split], X_scaled[split:]
    y_train, y_val = rf_probs[:split], rf_probs[split:]
    y_val_hard = rf_hard_labels[split:]

    student = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(len(FEATURE_COLUMNS),)),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(4, activation='softmax'),
    ])
    student.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    print("Entrenando red pequeña para imitar al Random Forest (destilación)...")
    student.fit(X_train, y_train, epochs=40, batch_size=32, verbose=2, validation_split=0.1)

    # Validar acuerdo real entre el modelo destilado y el Random Forest original.
    student_preds = np.argmax(student.predict(X_val, verbose=0), axis=1)
    agreement = accuracy_score(y_val_hard, student_preds)
    print(f"\nAcuerdo red destilada vs Random Forest en validación: {agreement:.3f}")
    label_names = {0: "Minimo", 1: "Leve", 2: "Moderado", 3: "Severo"}
    present_labels = sorted(set(y_val_hard.tolist()) | set(student_preds.tolist()))
    print(classification_report(
        y_val_hard, student_preds,
        labels=present_labels,
        target_names=[label_names[l] for l in present_labels]
    ))

    # Convertir a TFLite
    converter = tf.lite.TFLiteConverter.from_keras_model(student)
    tflite_model = converter.convert()
    os.makedirs(os.path.dirname(TFLITE_PATH), exist_ok=True)
    with open(TFLITE_PATH, "wb") as f:
        f.write(tflite_model)
    print(f"Modelo TFLite guardado en {TFLITE_PATH}")

    # Exportar los parámetros del scaler para poder normalizar en Kotlin
    # exactamente igual que en el entrenamiento (mean/scale por feature).
    scaler_params = {
        "features": FEATURE_COLUMNS,
        "mean": scaler.mean_.tolist(),
        "scale": scaler.scale_.tolist(),
    }
    with open(SCALER_JSON_PATH, "w") as f:
        json.dump(scaler_params, f, indent=2)
    print(f"Parámetros del scaler guardados en {SCALER_JSON_PATH}")
    print(f"\nAgreement={agreement:.3f} -- este número debe reportarse en el documento de tesis")
    print("como validación del modelo destilado, en vez de reportar el 'Completado' sin evidencia.")

if __name__ == "__main__":
    main()
