FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./backend/
# Copy frontend production distribution
COPY frontend/dist/ ./frontend/dist/

WORKDIR /app/backend

ENV PORT=8000
ENV HOST=0.0.0.0
ENV MONGODB_URL=mongodb://mongo:27017/buildpilot

EXPOSE 8000

CMD ["python", "run.py"]
