# Set base image and info
FROM ubuntu:latest

# Attach Shell
SHELL ["/bin/sh", "-c"]

# Port Forwarding
EXPOSE 2302/udp
EXPOSE 2303/udp
EXPOSE 2304/udp
EXPOSE 2305/udp

# Update Ubuntu to latest version/Install additional dependencies
RUN apt-get update \
    && \
    apt-get install -y \
    lib32stdc++6 \
    lib32gcc-s1 \
    wget \
    python3 \
    python3-pip \
    python3.12-venv

# Create arma3 user and configure server scripting entities
RUN useradd arma3
WORKDIR /home/arma3
ADD /dist/ /home/arma3
RUN tar -xvzf server_config.tar.gz
RUN rm server_config.tar.gz

# Configure Python environment
RUN python3 -m venv .venv
RUN source .venv/bin/activate
RUN python3 -m pip install -r requirements.txt

# Switch to arma3 user
USER arma3
