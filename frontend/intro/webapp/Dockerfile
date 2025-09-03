# ---- Stage 1: Build the frontend ----
FROM docker.io/node:18-alpine AS build
WORKDIR /app

# Build args (set at docker build --build-arg ...)
ARG REACT_APP_APIGW_BASE_URL=https://meity-auth.ulcacontrib.org
ARG BASE_URL=https://bhashini.gov.in
ARG APIGW_URL=https://meity-auth.ulcacontrib.org

# Make args available to build process
ENV REACT_APP_APIGW_BASE_URL=${REACT_APP_APIGW_BASE_URL}
ENV BASE_URL=${BASE_URL}
ENV APIGW_URL=${APIGW_URL}

COPY package*.json ./
RUN if [ -f package-lock.json ]; then \
      npm ci --legacy-peer-deps; \
    else \
      npm install --legacy-peer-deps; \
    fi

COPY . .
ENV NODE_OPTIONS=--openssl-legacy-provider
RUN npm run build   # React → /app/build (or Vite → /app/dist)

# ---- Stage 2: Serve with Nginx ----
FROM docker.io/nginx:1.25-alpine

# Pass through same values as runtime ENV too
ARG REACT_APP_APIGW_BASE_URL=https://meity-auth.ulcacontrib.org
ARG BASE_URL=https://bhashini.gov.in
ARG APIGW_URL=https://meity-auth.ulcacontrib.org

ENV REACT_APP_APIGW_BASE_URL=${REACT_APP_APIGW_BASE_URL}
ENV BASE_URL=${BASE_URL}
ENV APIGW_URL=${APIGW_URL}

# Copy build output (adjust to /app/dist if Vite)
COPY --from=build /app/build /usr/share/nginx/html

COPY ./nginx_fe_dev.conf /etc/nginx/conf.d/default.conf
COPY ./env-export.sh /docker-entrypoint.d/10-env-export.sh
RUN chmod +x /docker-entrypoint.d/10-env-export.sh

HEALTHCHECK CMD wget -qO- http://127.0.0.1/ >/dev/null 2>&1 || exit 1

