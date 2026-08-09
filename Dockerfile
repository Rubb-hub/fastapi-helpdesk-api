# Base image
FROM python:3.12-slim

# Avoid generating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Show logs immediately
ENV PYTHONUNBUFFERED=1

# Working directory inside the container
WORKDIR /app

# Copy dependencies first (better Docker cache)
COPY requirements.txt .

# Install dependencies only on image buildd
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start application -- 0.0.0.0 local conection
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 