# Use Python 3.12 base image
FROM python:3.12-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    pkg-config \  
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
COPY wait-for-db.sh .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Final image
FROM python:3.12-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    mariadb-client \ 
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"


# Copy wait-for-db script and make executable
COPY --from=builder /wait-for-db.sh /wait-for-db.sh 
RUN chmod +x /wait-for-db.sh  


# Set up application
WORKDIR /app
COPY . .

# Change working dir to where manage.py is located
WORKDIR /app/subscription_manager

# Collect static files
RUN python manage.py collectstatic --noinput

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "subscription_manager.wsgi:application"]