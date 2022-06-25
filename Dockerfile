FROM python:3.10-slim-buster AS base

RUN apt-get update \
    && apt-get upgrade -y
#    && apt-get install -y \
#    psycopg2 \
#    --no-install-recommends

RUN mkdir -p /src
WORKDIR /src

RUN pip install --upgrade pip poetry
RUN poetry config virtualenvs.create false
RUN poetry config experimental.new-installer false

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry install
COPY ./ /src/
RUN poetry install


CMD ["/bin/bash"]
