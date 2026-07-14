FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN groupadd --system --gid 1001 veriq \
    && useradd --system --uid 1001 --gid veriq --create-home veriq
COPY requirements.txt ./
RUN pip install --no-cache-dir --requirement requirements.txt
COPY app ./app
RUN mkdir -p /data && chown -R veriq:veriq /app /data

USER veriq
ENV VERIQ_DB_PATH=/data/veriq_mvp.db
ENV VERIQ_ALLOWED_ORIGINS=http://localhost:3000
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"]
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
