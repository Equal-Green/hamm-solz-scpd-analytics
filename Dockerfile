# SCPD Analytics — Streamlit dashboard, containerized for always-on hosting (Railway).
# Runs the exact same app as `streamlit run dashboard/app.py`; only difference is
# it binds to Railway's injected $PORT on 0.0.0.0 and never sleeps.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dependencies first for layer caching.
COPY requirements.txt ./
RUN pip install -r requirements.txt

# App source (incl. the prebuilt data/scpd.duckdb, which is committed).
COPY . .

# Railway provides $PORT at runtime; default to 8501 for local `docker run`.
ENV PORT=8501
EXPOSE 8501

# Shell form so $PORT expands. address 0.0.0.0 is required inside a container.
CMD streamlit run dashboard/app.py \
    --server.port=${PORT} \
    --server.address=0.0.0.0 \
    --server.headless=true
