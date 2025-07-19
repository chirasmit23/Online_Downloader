FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    chromium chromium-driver \
    wget curl unzip gnupg \
    fonts-liberation libappindicator3-1 libasound2 libnspr4 libnss3 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libatk-bridge2.0-0 \
    libgtk-3-0 libgbm1 libxss1 libxtst6 libxcb1 libx11-6 libxext6 \
    && rm -rf /var/lib/apt/lists/*
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV PYTHONUNBUFFERED=TRUE
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 10000
CMD ["gunicorn", "-b", "0.0.0.0:10000", "main:app"]
