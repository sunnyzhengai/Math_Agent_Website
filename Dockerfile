# ---------- Build stage ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# System deps (build & runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install deps to a wheelhouse (faster final image)
COPY requirements.txt .
RUN pip wheel --wheel-dir=/wheels -r requirements.txt

# ---------- Runtime stage ----------
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    TELEMETRY_ENABLED=true \
    TELEMETRY_PATH=logs/telemetry.jsonl \
    TELEMETRY_MAX_BYTES=5242880 \
    TELEMETRY_SAMPLE_RATE=0.25 \
    SERVER_ID=prod \
    APP_VERSION=0.2.0

WORKDIR /app

# Minimal runtime libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy deps from builder
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy app
COPY . .

# Make sure log dirs exist
RUN mkdir -p logs/telemetry.rotate

# Non-root (optional)
RUN useradd -ms /bin/bash appuser
USER appuser

# Expose port for platforms (Fly/Render)
EXPOSE 8080

# Start server (gunicorn + uvicorn workers)
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "api.server:app", \
     "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "60", "--access-logfile", "-"]
