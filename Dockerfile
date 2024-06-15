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
    python3

# Create arma3 user and steamcmd directory
RUN useradd arma3
WORKDIR /home/arma3

# Download steamcmd tarball
VOLUME /steamcmd
WORKDIR /home/arma3/steamcmd
# RUN wget http://media.steampowered.com/installer/steamcmd_linux.tar.gz

# # Extract steamcmd tarball
# RUN tar -xvzf steamcmd_linux.tar.gz

# Switch to arma3 user
USER arma3
