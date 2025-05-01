# python 3.13 image
FROM python:3.13-slim-bookworm

ARG TARGETARCH
RUN echo "Building for Target Arch: ${TARGETARCH}"

USER root
WORKDIR /tmp

RUN apt-get update && \
    apt-get install -y -f -m curl nodejs zip unzip wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    curl -sSL https://install.python-poetry.org | python3 -

RUN python3 -m pip install --no-cache-dir poetry
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /root

ARG TERRAFORM_VERSION=1.11.4
ARG TERRAFORM_CDK_VERSION=0.20.12
ARG TERRAFORM_BINARY_NAME="/usr/local/bin/terraform"
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    npm install --global cdktf-cli@${TERRAFORM_CDK_VERSION} @types/node && \
    wget -O tf.zip "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_${TARGETARCH}.zip" && \
    unzip tf.zip && \
    mv terraform ${TERRAFORM_BINARY_NAME} && \
    rm tf.zip && \
    chmod 777 ${TERRAFORM_BINARY_NAME}

WORKDIR /tmp

ARG CICD_PATH=.cicd/python
ARG CST_PATH=lib/python/cloud_server_tool

ARG CICD_NAME=cicd
ARG CST_NAME=cloud_server_tool

WORKDIR /tmp
COPY ${CICD_PATH}/pyproject.toml ${CICD_PATH}/poetry.lock /tmp/${CICD_NAME}/
COPY ${CST_PATH}/pyproject.toml ${CST_PATH}/poetry.lock /tmp/${CST_NAME}/

RUN cd /tmp/${CICD_NAME} && python3 -m pip install poetry-plugin-export &&  \
    poetry export --with dev --without-hashes --output requirements.txt &&  \
    python3 -m pip install -r /tmp/${CICD_NAME}/requirements.txt &&  \
    cd /tmp/${CST_NAME} && poetry export --with dev --without-hashes --output requirements.txt && \
    python3 -m venv /root/venvs/${CST_NAME} && \
    /root/venvs/${CST_NAME}/bin/python -m pip install -r /tmp/${CST_NAME}/requirements.txt && \
    rm -rf /tmp/* /root/.cache/*
