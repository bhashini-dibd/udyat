FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_PREFER_BINARY=1
    # Removed PIP_ONLY_BINARY=:all: to allow source builds if needed

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency files first
COPY requirements.txt constraints.txt ./

# --- Patch the obsolete pin if present ---
# Replace exact pin 0.5.3 with a known-good available version
RUN sed -i 's/^editdistance==0\.5\.3$/editdistance==0.8.1/' /app/requirements.txt

# Install deps with constraints
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-build-isolation -r /app/requirements.txt -c /app/constraints.txt

# App code
COPY . .

# NLTK data
RUN python -m nltk.downloader wordnet

# Start script
RUN install -m 0755 start.sh /usr/bin/start.sh
CMD ["/usr/bin/start.sh"]

