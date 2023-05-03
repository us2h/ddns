FROM python:3.11-slim-buster

WORKDIR /app

# Python optimizations
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt

RUN set -eux \
    pip install --upgrade pip setuptools wheel \
    && pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . .

ENTRYPOINT ["python", "app.py"]
