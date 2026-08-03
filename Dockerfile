# Inception runtime — the running Genesis service.
FROM python:3.12-slim
WORKDIR /app
RUN useradd -u 10001 -m app && mkdir -p /data && chown 10001:10001 /data
COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY tools/ ./tools/
COPY examples/ ./examples/
COPY schemas/ ./schemas/
RUN pip install --no-cache-dir "fastapi>=0.110" "uvicorn>=0.29" "jsonschema>=4.18" pyyaml
ENV PYTHONPATH=/app/src INCEPTION_LOG=/data/events.jsonl PYTHONUNBUFFERED=1
USER 10001:10001
EXPOSE 8731
# uvicorn serves the FastAPI app; the durable event log lives on the mounted /data PVC.
CMD ["uvicorn", "inception.service:app", "--host", "0.0.0.0", "--port", "8731"]
