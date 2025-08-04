# Kickbase Ultimate Analyzer - Dockerfile
FROM python:3.11-slim

# Metadata
LABEL maintainer="Kickbase Ultimate Analyzer"
LABEL version="1.0.0"
LABEL description="Comprehensive Kickbase Fantasy Football Analysis Tool"

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Build tools
    build-essential \
    gcc \
    g++ \
    # System libraries
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    libpng-dev \
    zlib1g-dev \
    # Database
    sqlite3 \
    libsqlite3-dev \
    postgresql-client \
    # Web scraping
    chromium \
    chromium-driver \
    # Network tools
    curl \
    wget \
    # Security tools
    tor \
    proxychains4 \
    # Utilities
    git \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd --create-home --shell /bin/bash app

# Set work directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p kickbase_data exports logs cache temp && \
    chown -R app:app /app

# Copy configuration files
COPY config.yaml .
COPY .env.template .env

# Set executable permissions
RUN chmod +x kickbase_ultimate_analyzer.py

# Configure Chrome for headless operation
RUN echo '#!/bin/bash\n\
chromium \
  --no-sandbox \
  --headless \
  --disable-gpu \
  --disable-dev-shm-usage \
  --disable-extensions \
  --disable-plugins \
  --disable-images \
  --disable-javascript \
  --remote-debugging-port=9222 \
  "$@"' > /usr/local/bin/chrome-headless && \
    chmod +x /usr/local/bin/chrome-headless

# Configure Tor (if needed)
RUN echo "socks5 127.0.0.1 9050" >> /etc/proxychains4.conf

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python3 -c "from kickbase_ultimate_analyzer import Config; print('OK')" || exit 1

# Switch to app user
USER app

# Expose ports
EXPOSE 8050 8080

# Default command
CMD ["python3", "kickbase_ultimate_analyzer.py", "--mode", "scheduler"]

# Alternative entry points
# For one-time analysis:
# docker run kickbase-analyzer python3 kickbase_ultimate_analyzer.py --mode full
#
# For quick analysis:
# docker run kickbase-analyzer python3 kickbase_ultimate_analyzer.py --mode quick
#
# For interactive shell:
# docker run -it kickbase-analyzer /bin/bash