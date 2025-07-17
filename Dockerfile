
FROM python:3.9-slim

WORKDIR /app


COPY requirements.txt .


RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libpng-dev \
    fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 5000


ENV FLASK_ENV=production

# Chạy ứng dụng Flask
CMD ["python", "app.py"]