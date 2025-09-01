# ---------- Build stage ----------
FROM node:16-alpine AS builder
WORKDIR /app

# native build deps (safe to have)
RUN apk add --no-cache python3 make g++

# Copy manifests AND local tarballs referenced by package.json
COPY package*.json ./
# adjust path if the tgz is elsewhere
COPY ./react-transliterate-2.2.9.tgz ./ 

# Install with relaxed peer-deps (React 17 vs ^16 peer)
RUN npm config set legacy-peer-deps true && \
    npm config set strict-peer-deps false && \
    if [ -f package-lock.json ]; then \
      npm ci --legacy-peer-deps; \
    else \
      npm install --legacy-peer-deps; \
    fi

# Copy source and build
COPY . .

# Build-time args (pass with --build-arg)
ARG REACT_APP_BASE_URL
ARG REACT_APP_APIGW_BASE_URL

# Make them available during build (CRA only embeds REACT_APP_* automatically)
ENV REACT_APP_BASE_URL=$REACT_APP_BASE_URL \
    REACT_APP_APIGW_BASE_URL=$REACT_APP_APIGW_BASE_URL \
    NODE_ENV=production

RUN npm run build

# ---------- Runtime stage ----------
FROM docker.io/nginx:1.17.4-alpine
COPY --from=builder /app/build /usr/share/nginx/html

# Optional runtime substitution script + nginx config
COPY ./env-export.sh /usr/bin/env-export.sh
RUN chmod +x /usr/bin/env-export.sh
COPY ./nginx_fe_dev.conf /etc/nginx/conf.d/default.conf

CMD ["/bin/sh","-c","/usr/bin/env-export.sh && nginx -g 'daemon off;'"]

