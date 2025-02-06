# Use official Python image as a base
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

COPY .env /app/.env

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the PYTHONPATH to include /app directory
ENV PYTHONPATH=/app

# Expose port for FastAPI
EXPOSE 8000

# Start FastAPI application and Kafka producer with metrics generation
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD python3 app/metrics_producer.py & uvicorn app.main:app --host 0.0.0.0 --port 8000
