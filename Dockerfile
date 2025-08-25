FROM python:3.13-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and environment file
COPY main.py .
COPY .env .

# Run the application
CMD ["python", "main.py"]
