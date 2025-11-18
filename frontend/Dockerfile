FROM alpine:3.22

# setup python and node
RUN apk add --no-cache nodejs pnpm curl
RUN mkdir /app
WORKDIR /app

# install dependendcy



# frontend
COPY package.json /app/package.json
RUN pnpm install

COPY . /app/

ENTRYPOINT [ "pnpm", "run", "dev" ]
# ENTRYPOINT [ "sleep", "10000" ]
