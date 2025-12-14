# Use Python 3.11 slim image as base
FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=mock_server.py

# Copy requirements file
COPY requirements-mock.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements-mock.txt

# Copy the application code
COPY mock_server.py .

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "mock_server.py"]
