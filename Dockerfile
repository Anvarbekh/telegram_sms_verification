FROM python:3.11-slim

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

# install OS-level build deps required by some Python packages (psycopg2, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# copy and upgrade pip/setuptools/wheel to avoid build issues
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


