FROM --platform=linux/amd64 debian:stable-slim

WORKDIR /app

COPY blackbox /app/

RUN chmod +x /app/blackbox
RUN apt-get update