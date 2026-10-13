FROM python:3.12-slim

# Prevent Python from creating .pyc files
# and ensure logs appear immediately.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Application directory
WORKDIR /app

# Install Python dependencies first
# to improve Docker layer caching.
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Create runtime directories if they don't exist.
RUN mkdir -p \
    data/raw \
    data/processed \
    data/documents \
    database

# FastAPI
EXPOSE 8000

# Streamlit
EXPOSE 8501

# Default command.
# Docker Compose will override this for each service.
CMD ["uvicorn", "api_app:app", "--host", "0.0.0.0", "--port", "8000"]