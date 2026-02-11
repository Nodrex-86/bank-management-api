# 1. Basis-Image (Python)
FROM python:3.12-slim

# 2. Arbeitsverzeichnis im Container
WORKDIR /app

# 3. Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Den restlichen Code kopieren
COPY . .

# 5. Port 8000 freigeben
EXPOSE 8000

# 6. Startbefehl für die Cloud/Docker
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]