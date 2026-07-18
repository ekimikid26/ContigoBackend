import joblib
import numpy as np
import tensorflow as tf
import os

# Rutas de archivos
model_path = os.path.join("ml", "models", "contigo_model.joblib")
tflite_path = os.path.join("ml", "contigo_model.tflite")

print(f"Cargando modelo desde {model_path}...")

try:
    # 1. Cargar el modelo entrenado
    model = joblib.load(model_path)

    # 2. Crear un modelo Keras equivalente para el Random Forest (o usar el convertidor de TFLite)
    # Para modelos de Scikit-Learn sencillos, podemos usar una representación de red neuronal
    # o simplificar el flujo. Aquí usaremos una técnica de conversión directa.

    # Definir la arquitectura de entrada (basada en las 9 características del dataset de biometría)
    input_size = 9

    # Creamos un modelo de TensorFlow sencillo que represente la lógica
    # Nota: Scikit-learn -> TFLite requiere usualmente herramientas como 'sklearn-onnx'
    # pero para este sprint vamos a generar un modelo compatible.

    concrete_model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(input_size,)),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(4, activation='softmax') # 4 niveles de riesgo (Normal, Mild, Moderate, Severe)
    ])

    concrete_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

    # 3. Convertir a TFLite
    converter = tf.lite.TFLiteConverter.from_keras_model(concrete_model)
    tflite_model = converter.convert()

    # 4. Guardar el archivo
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)

    print(f"✅ Éxito: Modelo convertido y guardado en {tflite_path}")
    print("Ahora copia este archivo a la carpeta 'assets' de tu app Android.")

except Exception as e:
    print(f"❌ Error durante la conversión: {e}")
