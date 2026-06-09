FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN echo "deb http://mirror-linux.runflare.com/debian trixie main" > /etc/apt/sources.list && \
    echo "deb http://mirror-linux.runflare.com/debian-security trixie-security main" >> /etc/apt/sources.list && \
    apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
# دستور اصلاح شده:
RUN pip install --no-cache-dir -r requirements.txt


COPY . .
