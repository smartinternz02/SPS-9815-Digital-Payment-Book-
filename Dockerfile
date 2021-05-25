FROM python:3.9-alpine
WORKDIR /app
ADD . /app
RUN set -e; \
        apk add --no-cache --virtual .build-deps \
        gcc \
        libc-dev \
        linux-headers \
        mariadb-dev \
        python3-dev \
        postgresql-dev \
    ;
RUN apk add build-base
RUN apk add alpine-sdk
COPY requirements.txt /app
RUN pip install -r requirements.txt
CMD [ "python","app.py"]  