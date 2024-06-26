FROM python:3.9-alpine3.13
LABEL maintainer="boatbot.seven"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN apk add --update --no-cache postgresql-dev gcc musl-dev && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt

RUN adduser \
        --disabled-password \
        --home /home/django-user \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user
