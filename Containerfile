FROM python:3-alpine AS build

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apk add --no-cache git

COPY requirements.txt .
RUN pip install --user --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3-alpine

# Set it as an environment variable inside the image
ARG COMMIT_SHA
ENV GIT_COMMIT_SHA=$COMMIT_SHA

WORKDIR /app

COPY --from=build /install /usr/local

COPY main.py .

CMD ["python", "main.py"]
