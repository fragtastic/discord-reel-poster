FROM python:3-alpine as build

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apk add --no-cache git

COPY requirements.txt .
RUN pip install --user --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3-alpine

WORKDIR /app

COPY --from=build /install /usr/local

COPY main.py .

CMD ["python", "main.py"]
