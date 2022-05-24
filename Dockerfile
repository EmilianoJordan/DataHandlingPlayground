FROM python:3.9.8-slim-buster AS base

RUN apt-get update && apt-get upgrade -y

RUN mkdir -p /src
WORKDIR /src

COPY setup.py setup.py

RUN pip install -e ".[dev]"

CMD ["/bin/bash"]
