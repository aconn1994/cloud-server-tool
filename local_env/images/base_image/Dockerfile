# python 3.13 image
FROM python:3.13-slim-bookworm

USER root
WORKDIR /tmp

RUN apt-get update \
    curl -sSL https://install.python-poetry.org | python3 -

RUN python3 -m pip install --no-cache-dir poetry
ENV PATH="${PATH}:/root/.local/bin"

ARG CST_PATH=lib/python/cst
ARG CST_NAME=cst

WORKDIR /tmp
COPY ${CST_PATH}/pyproject.toml ${CST_PATH}/poetry.lock /tmp/${CST_NAME}/

RUN cd /tmp/${CST_NAME} && python3 -m pip install poetry-plugin-export && poetry export --with dev --without-hashes --output requirements.txt && \
    python3 -m venv /root/venvs/${CST_NAME} && \
    /root/venvs/${CST_NAME}/bin/python -m pip install -r /tmp/${CST_NAME}/requirements.txt && \
    rm -rf /tmp/* /root/.cache/*


# docker build -t local_env:latest .
# docker run --name local_env -it local_env