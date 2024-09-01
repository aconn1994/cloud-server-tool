# Set base image and info
FROM ubuntu:latest

# Attach Shell
SHELL ["/bin/bash", "-c"]

# Port Forwarding
EXPOSE 2344/udp 2344 2345
EXPOSE 2302/udp 2303/udp 2304/udp 2305/udp 2306/udp

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
RUN python3 -m pip install -r requirements.txt --break-system-packages

# Add steamcmd directory
WORKDIR /home/arma3/steamcmd
RUN wget -qO- 'http://media.steampowered.com/installer/steamcmd_linux.tar.gz' | tar zxf - -C /home/arma3/steamcmd
RUN chmod 777 /home/arma3/steamcmd
RUN chmod 777 /home/arma3/steamcmd/linux32/steamcmd
RUN sh ./steamcmd.sh <<< "exit"

# Switch to arma3 user
WORKDIR /home/arma3
# USER arma3