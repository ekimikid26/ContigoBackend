FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Railway inyecta la variable PORT automáticamente.
# Usamos esta sintaxis para asegurarnos de que se use.
CMD uvicorn main:app --host 0.0.0.0 --port $PORT