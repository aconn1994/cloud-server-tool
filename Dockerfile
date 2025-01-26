# Set base image and info
FROM ubuntu:latest

# Attach Shell
SHELL ["/bin/bash", "-c"]

# Port Forwarding
EXPOSE 2302/udp 2303/udp 2304/udp 2305/udp 2306/udp

# Update Ubuntu to latest version/Install additional dependencies
RUN apt-get update \
    && \
    apt-get install -y \
    lib32stdc++6 \
    lib32gcc-s1 \
    wget \
    python3

# Set Environment Variables
ENV DIR_STEAMCMD steamcmd
ENV DIR_LOCAL_GAME arma3
ENV DIR_LOCAL_MOD mods
ENV DIR_KEYS_DIR keys
ENV DIR_STEAM_MOD_DOWNLOAD steamapps/workshop/content/107410
ENV STEAM_USERNAME <your-steam-username>
ENV STEAM_PASSWORD <your-steam-password>
ENV GAME_SERVER_ID 233780
ENV GAME_WORKSHOP_ID 107410

# Create arma3 user and configure server scripting entities
RUN useradd arma3
WORKDIR /home/arma3
ADD /dist/ /home/arma3
RUN tar -xvzf server_config.tar.gz
RUN rm server_config.tar.gz

# Add steamcmd directory
WORKDIR /home/arma3/steamcmd
RUN wget -qO- "http://media.steampowered.com/installer/steamcmd_linux.tar.gz" | tar zxf - -C /home/arma3/steamcmd
RUN chmod 777 /home/arma3/steamcmd
RUN chmod 777 /home/arma3/steamcmd/linux32/steamcmd

# Run Arma 3 install
WORKDIR /home/arma3
CMD ["python3", "install"]