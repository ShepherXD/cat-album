# ---------- base ----------
FROM alpine:3.22 AS base

# setup python and node
RUN apk add --no-cache nodejs pnpm curl
RUN mkdir /app
WORKDIR /app

# frontend
COPY package.json /app/package.json
RUN pnpm install

COPY . /app/

# ---------- dev ----------
FROM base AS dev
ENTRYPOINT [ "pnpm", "run", "dev" ]
# ENTRYPOINT [ "sleep", "10000" ]

# ---------- prod ----------
FROM base AS prod

# Caddy 
RUN apk add --no-cache caddy

# Compile & Build
RUN pnpm run build-only

COPY Caddyfile /etc/Caddyfile
ENTRYPOINT ["caddy","run", "-c", "/etc/Caddyfile" ]





