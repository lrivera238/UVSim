# Use Python 3.9 as the base image
FROM python:3.11.9

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV FLASK_APP=app/app.py
ENV FLASK_ENV=production
ENV PORT=5000
ENV API_BASE=/api

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD exec gunicorn --bind :${PORT} --workers 1 --threads 8 --timeout 0 run:app