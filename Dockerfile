FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Forzamos el puerto 8080 que es el estándar más estable en Railway
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]