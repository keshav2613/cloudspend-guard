FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Create non-root runtime user
RUN addgroup --system app && \
    adduser --system --ingroup app app

# Install dependencies first for better Docker layer caching
COPY pyproject.toml .

RUN pip install --no-cache-dir .

# Copy application source
COPY --chown=app:app app ./app

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]