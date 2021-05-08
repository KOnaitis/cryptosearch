FROM python:3.9

ARG USER=cryptosearch
ARG ROOT=/home/cryptosearch

COPY . $ROOT

RUN apt-get update
RUN useradd -ms /bin/bash $USER
RUN chown -R $USER: $ROOT

RUN pip install --upgrade pip gunicorn

USER $USER
WORKDIR $ROOT

RUN make install

EXPOSE 8000
