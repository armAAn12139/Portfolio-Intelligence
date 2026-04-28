FROM python:3.10-slim

# Env optimizations
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies (critical for numpy/scipy)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    gfortran \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip (important for wheel installs)
RUN pip install --upgrade pip

# Copy requirements first (layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Streamlit config (prevents random behavior in container)
RUN mkdir -p /root/.streamlit && \
    echo "[server]\nheadless = true\nenableCORS = false\nport = 8501\naddress = \"0.0.0.0\"" > /root/.streamlit/config.toml

# Expose port
EXPOSE 8501

# Run app
CMD ["streamlit", "run", "app.py"]
