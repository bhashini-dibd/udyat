# Use an official, public base
FROM docker.io/library/python:3.11-slim AS app

# Safer, smaller builds
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# (Optional) system deps if you build native wheels
# Keep minimal; add more only if your libs need them
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
 && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for layer caching
COPY requirements.txt /app/requirements.txt

# If your requirements list "opencv-python", replace with "opencv-python-headless"
# so you don't pull GUI libs inside the container.
# This no-op if not present.
RUN sed -i 's/^opencv-python\(\(==\|>=\).*\)\?$/opencv-python-headless\1/' requirements.txt || true

# Install deps (and uwsgi)
RUN pip3 install -r requirements.txt && pip3 install uwsgi

# Now copy the rest of the app
COPY . /app

# Start script
COPY start.sh /usr/bin/start.sh
RUN chmod +x /usr/bin/start.sh

EXPOSE 8000
CMD ["/usr/bin/start.sh"]

