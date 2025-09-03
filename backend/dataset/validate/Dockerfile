# ---- Base image ----
FROM python:3.10-slim

# Env
ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1

# ---- System deps (PyICU, Pillow, ffmpeg) ----
# Note: trixie uses libtiff-dev (not libtiff5)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libicu-dev \
    zlib1g-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    libtiff-dev \
    libfreetype6-dev \
    libopenjp2-7-dev \
    libwebp-dev \
    ffmpeg \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# ---- Workdir ----
WORKDIR /app

# ---- Python deps (cache-friendly) ----
# Copy only requirements first, so deps layer is cached when app code changes
COPY requirements.txt /app/requirements.txt

# Upgrade build tooling and install deps
# (Your requirements already set numpy==1.26.4 which is py310-compatible)
RUN python -m pip install --upgrade pip wheel setuptools \
 && pip install --no-cache-dir -r requirements.txt

# ---- App code ----
COPY . /app

# ---- Optional model/artifact downloads at build ----
# If you prefer to download at container start, move this into start.sh
RUN polyglot download transliteration2.hi || true

# ---- Entrypoint ----
COPY start.sh /usr/bin/start.sh
RUN chmod +x /usr/bin/start.sh

CMD ["/usr/bin/start.sh"]

