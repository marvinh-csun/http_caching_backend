FROM python:3.11-bullseye

WORKDIR /code
COPY . /code

RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt 

EXPOSE 5010
