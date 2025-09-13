# ---- Stage 1: Build the frontend ----
FROM docker.io/node:18-alpine AS build
WORKDIR /app

ARG REACT_APP_APIGW_BASE_URL=https://meity-auth-test.ulcacontrib.org
ARG BASE_URL=https://udyat.bhashini.co.in/ulca
ARG APIGW_URL=https://meity-auth-test.ulcacontrib.org

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
ENV NODE_OPTIONS="--openssl-legacy-provider"
RUN npm run build

# ---- Stage 2: Serve with Nginx ----
FROM docker.io/nginx:1.25-alpine

ARG REACT_APP_APIGW_BASE_URL=https://meity-auth-test.ulcacontrib.org
ARG BASE_URL=https://udyat.bhashini.co.in/ulca
ARG APIGW_URL=https://meity-auth-test.ulcacontrib.org

ENV REACT_APP_APIGW_BASE_URL=${REACT_APP_APIGW_BASE_URL}
ENV BASE_URL=${BASE_URL}
ENV APIGW_URL=${APIGW_URL}

# Optional: install curl for healthcheck (busybox wget isn't always present)
RUN apk add --no-cache curl

COPY --from=build /app/build /usr/share/nginx/html

COPY ./nginx_fe_dev.conf /etc/nginx/conf.d/default.conf
COPY ./env-export.sh /docker-entrypoint.d/10-env-export.sh
RUN chmod +x /docker-entrypoint.d/10-env-export.sh

EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -fsS http://127.0.0.1/ >/dev/null || exit 1

