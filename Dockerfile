FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download es_core_news_md

COPY . .

EXPOSE 8001

CMD ["gunicorn", "camara_web.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "2", "--timeout", "120"]
