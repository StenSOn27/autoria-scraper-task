FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat-openbsd \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium

COPY . .

RUN dos2unix /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]