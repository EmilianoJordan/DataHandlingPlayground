FROM python:3.9.8-slim-buster AS base

RUN apt-get update \
    && apt-get upgrade -y
#    && apt-get install -y \
#    psycopg2 \
#    --no-install-recommends

RUN mkdir -p /src
WORKDIR /src

COPY setup.py setup.py

RUN pip install -e ".[dev]"

CMD ["/bin/bash"]
