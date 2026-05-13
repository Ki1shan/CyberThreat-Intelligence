FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create working directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -ms /bin/bash ctiuser
USER ctiuser

# Copy and install Python dependencies
COPY --chown=ctiuser:ctiuser requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY --chown=ctiuser:ctiuser . .

# Expose Flask default port
EXPOSE 5000

# Run the application
CMD ["python", "run.py"]

