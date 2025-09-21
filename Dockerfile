# ---- Stage 1: Builder ----
FROM python:3.11-slim AS builder
WORKDIR /usr/src/app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Stage 2: Final Image ----
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY app.py .
RUN useradd --create-home appuser
USER appuser
ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 8080
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8080", "app:app"]