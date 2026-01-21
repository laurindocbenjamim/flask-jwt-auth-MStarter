# Use a specific version for stability
FROM python:3.12.3-slim

# 1. Install system-level build dependencies
# We use -slim and then install only what we need to keep the image small
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    cargo \
    && rm -rf /var/lib/apt/lists/*

# 2. Set the working directory for your APP code
WORKDIR /app

# 3. Create the virtual environment in a standard container path
RUN python3 -m venv /opt/venv

# 4. Activate the virtual environment for all subsequent steps
ENV PATH="/opt/venv/bin:$PATH"

# 5. Install/Upgrade Python-specific tools

# Update your existing RUN apt-get command to include libpq-dev
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    cargo \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel 
RUN pip3 install --no-cache-dir --upgrade psycopg2-binary==2.9.11


# 6. Copy and install dependencies
# Doing this before 'COPY . .' leverages Docker's layer caching
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 7. Copy your actual application code
COPY . .

# 8. Start the application

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8443"]
#CMD ["python3", "-m", "app.py"]
