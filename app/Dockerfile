FROM python:3-alpine

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# install additional packages
WORKDIR /data/app
COPY %APP_NAME%/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
