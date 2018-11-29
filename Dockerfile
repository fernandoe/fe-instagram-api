FROM fernandoe/docker-python:3.7.0-alpine3.8
LABEL maintainer="Fernando Espíndola <fer.esp@gmail.com>"

RUN apk add --no-cache \
        libxml2-dev \
        libxslt-dev \
        libffi-dev

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./docker/run.sh /run.sh
COPY ./src /app

WORKDIR /app

CMD ["/run.sh"]
