# -------- STAGE 1: Build --------
FROM python:3.10-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements
COPY requirements.txt .

# Install dependencies into a custom directory
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# -------- STAGE 2: Runtime --------
FROM python:3.10-slim

WORKDIR /app

# Copy only installed packages
COPY --from=builder /install /usr/local

# Copy app code
COPY . .

# Streamlit config
RUN mkdir -p /root/.streamlit && \
    echo "[server]\nheadless = true\nenableCORS = false\nport = 8501\naddress = \"0.0.0.0\"" > /root/.streamlit/config.toml

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
