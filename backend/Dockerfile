FROM alpine:3.22

# setup python and node
RUN apk add --no-cache python3 py3-pip curl
RUN mkdir /app
WORKDIR /app

# install dependendcy

# backend
COPY requirements.txt /app/requirements.txt
RUN pip3 install --break-system-packages -r requirements.txt

COPY . /app/

ENTRYPOINT [ "uvicorn", "main:app", "--host","0.0.0.0", "--reload" ]
