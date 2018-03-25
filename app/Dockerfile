FROM python:3.6.4-alpine

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache postgresql-dev \
    && pip install psycopg2==2.7.4 \
    && apk del build-deps

# install application requirements
WORKDIR /data/app
COPY %APP_NAME%/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
